#!/usr/bin/env python3
"""Signed-RUN reproduction packet, v2.4 (Mutual Benefit Collective issue #21).

v2.4 moves the pin to a covenant commit with the ally fix (A447: only one of the operator's own registered keys may
authorize a RUN) and the corrected refusal text (A446), so case C1 is now expected to be REFUSED. It adds case
10_planted_json (capitaharlock's question, HF 191990 #2: a json.py planted beside the approved script must not load)
and the break no_isolation (the launch without -I, which must load it). The pinned set gains pairstore_excl.py,
which the durable nonce store (A444) imports, and the nonce store is pointed into the run's temporary root. The
list of files loaded from the source folder is now taken after the cases, so a lazy import is seen too.

v2.1 changed only how two observations are read on Windows; v2.2 adds two setup/classification guards from
DeepSeek's review (see CHANGES.md). v2.3 changes only case 4b's tailnet address, to 100.127.255.254 (the end of
100.64.0.0/10), and expected.json's wording of it. No expected outcome changed from v2's.

ONE COMMAND (after setup, see README.md)
    python3 run_packet.py --covenant PATH          (Windows: py -3 run_packet.py --covenant PATH)

PATH is a git clone of https://github.com/LAWLESS1987/covenant that contains the pinned commit below, or a folder
holding the nine covenant files listed in SOURCE_FILES (for example the unpacked GitHub zip of that commit). Every
file must match the git blob hash recorded below, or nothing runs (exit 2).

WHAT IT DOES
  * Copies the nine pinned covenant files (from the git object store when PATH is a clone; the working tree is not
    read) into a new temporary folder. PATH is only read.
  * For each of twelve VARIANTS (the pinned code and eleven deliberately broken copies) it starts one fresh Python
    process (the worker) that runs the fifteen cases against that copy.
  * A case is observed only through execution evidence: which marker file the scripts wrote, how many launches the
    hands attempted and with which arguments (audit event subprocess.Popen), and how many times the worker opened
    the script file while the door handled the request (audit event open).
  * It compares every observation with expected.json (v2.4's committed before its first run), prints a table, writes
    the raw record to an output folder, and exits 0 only when all twelve variants match.

WHAT IT NEEDS
  Python 3.10 or newer with flask and cryptography (the covenant core imports both). git only when PATH is a clone.
  No network after setup, no account, no key of ours: the signing keys are RSA keys generated in memory for the run.

EXIT CODES  0 all as pre-registered | 1 an observation differs | 2 could not run | 3 a fixture was inconclusive

What it does not test is in README.md section 8.
"""
import argparse
import hashlib
import json
import os
import itertools
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time

PACKET_VERSION = "v2.4"
PIN = "ead187b2513fba7bce1404cf3678ae128f38b1b8"
REPO_URL = "https://github.com/LAWLESS1987/covenant"

# git blob hashes at PIN (git rev-parse PIN:FILE): every covenant module the worker imports, measured with an audit
# hook when the packet was built. The worker reports any other file it loads from the source folder.
SOURCE_FILES = {
    "covenant_daily_plan.py": "bbbf9738b97e49280d03471a37756096212a04ee",
    "covenant_mycelium.py": "4f4473a30894292ed191cc34fafecc1b95b758e7",
    "covenant_path_pattern.py": "ff394e611747a054e3707970dbf06745dd02b885",
    "covenant_quiet.py": "87eebf68fef95c3ab1ebf4c3d45191db74961c02",
    "covenant_semantic_judge.py": "20f6b67cee9f7657109011d16613e025476b9915",
    "covenant_tetsu_hands.py": "297396f951480a453d36ea072c84ac801bac4c04",
    "covenant_unified_v8.py": "54f3fbffe5c3a17c7609b45712c3f1c71e62e7bc",
    "covenant_watchdog.py": "bad40ce5f46cbae3d889efadfe37ecbc1224d5f6",
    "pairstore_excl.py": "27f6556795282def6b033af19db148189949d8f9",
}

# The deliberate breaks: each an exact text replacement in the temporary copy. Each text must occur exactly once in
# its file, or the run stops (exit 2) rather than test a variant that was not built.
_BIND_DOC = 'None when the bytes about to run hash to the approved run_sha256; else why the run is refused."""'
_VERIFY_DEF = ('def verify_operator_signature(pubkey_pem: str, method: str, path: str, body: bytes,\n'
               '                              nonce: str, timestamp: float, signature_b64: str) -> bool:\n'
               '    try:\n')
MUTATIONS = {
    "no_signature_check": ("covenant_unified_v8.py", "_may_run = _request_signed_by_registered(request)",
                           "_may_run = True"),
    "no_hash_check": ("covenant_tetsu_hands.py", _BIND_DOC, _BIND_DOC + "\n    return None"),
    "always_refuse": ("covenant_tetsu_hands.py", _BIND_DOC, _BIND_DOC + "\n    return 'always-refuse variant'"),
    "no_args_check": ("covenant_tetsu_hands.py", 'if run_sha256 is not UNBOUND and d["args"]:', "if False:"),
    "child_reopens": ("covenant_tetsu_hands.py", "code = sys.stdin.buffer.read()",
                      'code = open(os.path.join(WS, script), "rb").read()'),
    "extra_parent_read": ("covenant_tetsu_hands.py", "    ok, why, imports = screen(raw)\n",
                          '    open(p, "rb").read()\n    ok, why, imports = screen(raw)\n'),
    "no_body_digest": ("covenant_unified_v8.py", 'body_hash = hashlib.sha256(body or b"").hexdigest()',
                       'body_hash = hashlib.sha256(b"").hexdigest()'),
    "no_signature_verify": ("covenant_unified_v8.py", _VERIFY_DEF, _VERIFY_DEF + "        return True\n"),
    "no_registry_check": ("covenant_daily_plan.py", 'return False, "key is not a registered daily-plan signer"',
                          'who = "unregistered (packet break)"'),
    # v2.4 (capitaharlock, HF 191990 #2): the child started without -I, so the workshop (its working directory) is
    # on sys.path and a planted json.py shadows the standard library.
    "no_isolation": ("covenant_tetsu_hands.py", 'subprocess.run([sys.executable, "-I", "-c", RUNNER, ws, name]',
                     'subprocess.run([sys.executable, "-c", RUNNER, ws, name]'),
}
VARIANTS = {
    "pinned": [],
    "always_refuse": ["always_refuse"],
    "accept_everything": ["no_signature_check", "no_hash_check", "no_args_check", "child_reopens"],
    "no_signature_check": ["no_signature_check"],
    "no_hash_check": ["no_hash_check"],
    "no_args_check": ["no_args_check"],
    "child_reopens": ["child_reopens"],
    "extra_parent_read": ["extra_parent_read"],
    "no_body_digest": ["no_body_digest"],
    "no_signature_verify": ["no_signature_verify"],
    "no_registry_check": ["no_registry_check"],
    "no_isolation": ["no_isolation"],
}

# The scripts under test. Each writes its own marker inside the workshop (the hands let a script open files only
# there) and prints one line. sha256(APPROVED) is what the operator signs.
SCRIPTS = {
    "approved": b'with open("ran_approved.txt", "w") as fh:\n    fh.write("approved")\nprint("approved bytes ran")\n',
    "changed": b'with open("ran_changed.txt", "w") as fh:\n    fh.write("changed")\nprint("changed bytes ran")\n',
    "substitute": b'with open("ran_substitute.txt", "w") as fh:\n    fh.write("substitute")\nprint("substitute bytes ran")\n',
    # v2.4, case 10: the approved script for that case imports json, then writes the approved marker. Its first
    # version also printed getattr(json, "PLANTED", ...); the screen refuses the name getattr, so nothing ran in
    # v2.4 run 1. The marker ran_planted.txt already says whether the planted file loaded.
    "imports_json": b'import json\nwith open("ran_approved.txt", "w") as fh:\n    fh.write("approved")\nprint("approved bytes ran")\n',
}
# v2.4, case 10: planted beside the script as workshop/json.py. If it is imported it leaves its own marker.
PLANTED_JSON = b'PLANTED = True\nwith open("ran_planted.txt", "w") as fh:\n    fh.write("planted")\n'
CASES = ["1_signed_no_args", "2_changed_bytes", "2b_one_byte_added", "3_added_args", "3b_one_argument",
         "4_unsigned_loopback", "4b_unsigned_tailnet", "5a_swap_at_launch", "5b_swap_continuous",
         "6_body_changed_after_signing", "7_bad_signature_registered_key", "8_unregistered_key",
         "9_signed_without_hash", "10_planted_json", "C1_ally_key_default_scope"]


def blob_sha(data):
    """git's blob hash of these bytes (what `git hash-object` prints)."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def _norm(p):
    return os.path.normcase(os.path.abspath(os.fsdecode(p)))


def launch_args(argv, ws, name):
    """The arguments the child was given after the script name, from the launch as the audit hook saw it: a list on
    POSIX ([python, -I, -c, RUNNER, ws, name, *args]), one command-line string on Windows (v2.1).

    v2.4: "-c" is found where it is, not assumed at index 2. The no_isolation break drops -I, which moved it to index
    1, and on POSIX every such launch read as unrecognized (v2.4 run 3, WSL); Windows parses the joined string and
    was not affected."""
    ws = os.path.abspath(ws)
    if isinstance(argv, list):
        if "-c" in argv:
            i = argv.index("-c")
            if len(argv) >= i + 4 and argv[i + 2] == ws and argv[i + 3] == name:
                return argv[i + 4:]
        return ["<unrecognized launch>"]
    prefix = subprocess.list2cmdline([ws, name])
    i = argv.find(prefix)
    if i < 0:
        return ["<unrecognized launch>"]
    rest = argv[i + len(prefix):]
    return [t[1:-1] if len(t) >= 2 and t[0] == t[-1] == '"' else t for t in shlex.split(rest, posix=False)]


# ===================================================================== worker (one variant, one fresh process)

def worker(src, root):
    """Run the cases against the covenant files in `src`; print one JSON line. Everything it writes is under root."""
    src, root = os.path.abspath(src), os.path.abspath(root)
    sys.dont_write_bytecode = True
    events = {"popen": [], "net": [], "writes_outside": []}
    watch = {"path": None, "reads": 0}
    root_n = _norm(root)
    # v2.1: event ORDER comes from one counter, not a clock. v2 compared time.monotonic() values, whose resolution on
    # Windows is 15.6 ms, so a swap and the launch right after it read as simultaneous (v2's first run, runs/).
    seq = itertools.count()

    def audit(ev, args):
        if ev == "subprocess.Popen":
            # v2.1: on Windows the audit event carries the command line as ONE string (subprocess has already joined
            # it with list2cmdline); on POSIX, the argument list. Both are kept as given.
            cmd = args[1] if len(args) > 1 else args[0]
            argv = [str(a) for a in cmd] if isinstance(cmd, (list, tuple)) else str(cmd)
            events["popen"].append({"seq": next(seq), "argv": argv})
        elif ev.startswith("socket."):
            events["net"].append([ev, repr(args)[:160]])
        elif ev == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            p = _norm(args[0])
            if watch["path"] is not None and p == watch["path"]:
                watch["reads"] += 1
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else 0
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or \
                (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT)))
            if writing and not (p == root_n or p.startswith(root_n + os.sep)):
                events["writes_outside"].append(p)
    sys.addaudithook(audit)

    # Nothing of the caller's covenant configuration reaches the code under test; every path it would default to is
    # pointed into this run's temporary root before the modules are imported.
    for k in [k for k in os.environ if k.startswith("COVENANT_")]:
        del os.environ[k]
    os.environ["COVENANT_TETSU_WORKSHOP"] = os.path.join(root, "unused_default_workshop")
    os.environ["COVENANT_TETSU_HANDS_LEDGER"] = os.path.join(root, "unused_default_hands.jsonl")
    os.environ["COVENANT_TETSU_PROPOSALS"] = os.path.join(root, "unused_default_proposals")
    os.environ["COVENANT_MYCELIUM_PEERS"] = os.path.join(root, "no_allies.json")
    os.environ["COVENANT_MYCELIUM_LEDGER"] = os.path.join(root, "mycelium.jsonl")
    os.environ["COVENANT_NONCE_STORE"] = os.path.join(root, "nonce_store")   # v2.4: A444's durable nonce store
    sys.path.insert(0, src)

    import ast
    import importlib
    from unittest.mock import patch
    from flask import Flask, request
    import covenant_daily_plan as DP
    import covenant_mycelium as MY
    import covenant_tetsu_hands as H
    import covenant_unified_v8 as cov

    # The door's real HANDS branch, taken from this variant's core file exactly as covenant's own test_a430_run_sha256
    # does (the one `if first.upper().startswith('HANDS')` block), and executed in a Flask request context.
    with open(cov.__file__, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    found = [n for n in ast.walk(tree) if isinstance(n, ast.If) and ast.unparse(n.test) == "first.upper().startswith('HANDS')"]
    if len(found) != 1:
        raise SystemExit("expected exactly one HANDS branch in the core, found %d" % len(found))
    branch = compile(ast.Module(body=found[0].body, type_ignores=[]), cov.__file__, "exec")

    # Three throwaway RSA-2048 keys, in memory only: the operator (registered as a signer), a stranger (registered
    # nowhere), and an ally (registered as an ally with the default scope, for C1 only).
    op_key, op_pem = cov.sig_keygen()
    stranger_key, stranger_pem = cov.sig_keygen()
    ally_key, ally_pem = cov.sig_keygen()
    app = Flask("signed_run_packet")
    sha = {k: hashlib.sha256(v).hexdigest() for k, v in SCRIPTS.items()}

    def one_case(name):
        case = os.path.join(root, name)
        shop = os.path.join(case, "workshop")
        os.makedirs(shop)
        signers = os.path.join(case, "signers.json")
        with open(signers, "w", encoding="utf-8") as fh:
            json.dump({"packet-operator": op_pem}, fh)
        peers = os.path.join(case, "allies.json")
        if name == "C1_ally_key_default_scope":
            MY.register_ally("packet-ally", ally_pem, "the packet fixture", path=peers)
        probe = os.path.join(shop, "probe.py")
        disk = {"2_changed_bytes": SCRIPTS["changed"], "2b_one_byte_added": SCRIPTS["approved"] + b"\n",
                "10_planted_json": SCRIPTS["imports_json"]}.get(name, SCRIPTS["approved"])
        with open(probe, "wb") as fh:
            fh.write(disk)
        if name == "10_planted_json":
            with open(os.path.join(shop, "json.py"), "wb") as fh:
                fh.write(PLANTED_JSON)
        answer = {"3_added_args": "HANDS RUN probe.py --extra 1", "3b_one_argument": "HANDS RUN probe.py x"}.get(name, "HANDS RUN probe.py")
        addr = "100.127.255.254" if name == "4b_unsigned_tailnet" else "127.0.0.1"
        approved_for_case = sha["imports_json"] if name == "10_planted_json" else sha["approved"]
        payload = {"text": "please run it"} if name == "9_signed_without_hash" else {"run_sha256": approved_for_case}
        body = json.dumps(payload).encode("utf-8")
        if name.startswith("4"):
            headers = {}
        elif name == "6_body_changed_after_signing":
            headers = cov.sign_operator_request(op_key, op_pem, "POST", "/m/agent",
                                                json.dumps({"run_sha256": sha["changed"]}).encode("utf-8"))
        elif name == "7_bad_signature_registered_key":
            headers = cov.sign_operator_request(op_key, op_pem, "POST", "/m/agent", body)
            other = cov.sign_operator_request(op_key, op_pem, "POST", "/m/agent", b'{"text": "something else"}')
            headers["X-Operator-Signature"] = other["X-Operator-Signature"]
        elif name == "8_unregistered_key":
            headers = cov.sign_operator_request(stranger_key, stranger_pem, "POST", "/m/agent", body)
        elif name == "C1_ally_key_default_scope":
            headers = cov.sign_operator_request(ally_key, ally_pem, "POST", "/m/agent", body)
        else:
            headers = cov.sign_operator_request(op_key, op_pem, "POST", "/m/agent", body)

        swap = {"writes": 0, "errors": 0, "first_t": None}
        first_swap = threading.Event()
        stop = threading.Event()
        threads = []

        def write_substitute():
            tmp = probe + ".swap"
            with open(tmp, "wb") as fh:
                fh.write(SCRIPTS["substitute"])
            os.replace(tmp, probe)
            swap["writes"] += 1
            if swap["first_t"] is None:
                swap["first_t"] = next(seq)
                first_swap.set()

        def keep_swapping():
            while not stop.is_set():
                try:
                    write_substitute()
                except OSError:
                    swap["errors"] += 1
                time.sleep(0.001)

        def gate(text):                   # the quorum, stubbed to "clean" so only the binding logic decides
            if name == "5b_swap_continuous" and not threads:
                t = threading.Thread(target=keep_swapping, daemon=True)
                threads.append(t)
                t.start()
                first_swap.wait(10)       # the gate returns only after the first replacement is confirmed
            return "clean", "packet fixture: quorum stubbed"

        real_run = H.subprocess.run

        def swap_then_launch(*a, **k):    # 5a: after the hash check and the screen, at the launch itself
            write_substitute()
            return real_run(*a, **k)

        patches = [patch.object(H, "WORKSHOP", shop), patch.object(H, "LEDGER", os.path.join(case, "hands.jsonl")),
                   patch.object(H, "_gate", gate), patch.object(DP, "SIGNERS", signers),
                   patch.object(DP, "_seen_nonces", set()), patch.object(MY, "_seen", set()),
                   patch.object(MY, "PEERS", peers), patch.object(MY, "LEDGER", os.path.join(case, "mycelium.jsonl"))]
        if name == "5a_swap_at_launch":
            patches.append(patch.object(H.subprocess, "run", swap_then_launch))
        popen_before = len(events["popen"])
        scope = {"request": request, "answer": answer, "importlib": importlib,
                 "_request_signed_by_registered": cov._request_signed_by_registered,
                 "forum": [], "msgs": [], "_ask_fitted": lambda: ("done", {})}
        error = None
        for p in patches:
            p.start()
        watch["path"], watch["reads"] = _norm(probe), 0
        try:
            with app.test_request_context("/m/agent", method="POST", data=body, headers=headers,
                                          content_type="application/json", environ_base={"REMOTE_ADDR": addr}):
                exec(branch, scope)
        except Exception as e:            # noqa: BLE001 -- makes the case INCONCLUSIVE, never a refusal
            error = "%s: %s" % (type(e).__name__, str(e)[:300])
        finally:
            reads = watch["reads"]
            watch["path"] = None
            stop.set()
            for t in threads:
                t.join(5)
            for p in reversed(patches):
                p.stop()
        markers = {}
        for who in SCRIPTS:
            mp = os.path.join(shop, "ran_%s.txt" % who)
            if os.path.exists(mp):
                with open(mp, encoding="utf-8", errors="replace") as fh:
                    markers[who] = fh.read()
        with open(probe, "rb") as fh:
            on_disk = fh.read()
        planted_loaded = os.path.exists(os.path.join(shop, "ran_planted.txt"))
        launches = events["popen"][popen_before:]
        child_args = None
        if launches:
            child_args = launch_args(launches[0]["argv"], shop, "probe.py")
        swapped_before_launch = bool(launches) and swap["first_t"] is not None and swap["first_t"] < launches[0]["seq"]

        why = []
        if error:
            why.append("the harness raised: " + error)
        if len(markers) > 1:
            why.append("more than one marker: %s" % sorted(markers))
        if any(markers[w] != w for w in markers):
            why.append("a marker with the wrong content: %s" % markers)
        if name.startswith("5") and launches and not swapped_before_launch:
            why.append("a launch with no swap confirmed before it")
        if markers and not launches:          # v2.2 (DeepSeek): RAN_* means a marker AFTER a launch attempt
            why.append("a marker with no launch attempt")
        if planted_loaded and not launches:   # v2.4: the planted file can only load in a launched child
            why.append("the planted json.py marker with no launch attempt")
        if why:
            outcome = "INCONCLUSIVE"
        elif markers:
            outcome = "RAN_" + next(iter(markers)).upper()
        elif launches:
            outcome = "LAUNCH_NO_MARKER"
        else:
            outcome = "NOTHING"
        rec = scope.get("_rec") or {}
        return {
            "outcome": outcome, "inconclusive_why": why, "reads": reads, "launches": len(launches),
            "child_args": child_args, "markers": markers, "planted_loaded": planted_loaded,
            "swap": {"writes": swap["writes"], "errors": swap["errors"], "confirmed_before_launch": swapped_before_launch},
            "probe_on_disk_after": ([k for k, v in SCRIPTS.items() if v == on_disk] or ["other"])[0],
            "answer": answer, "caller_address": addr, "signed_headers": bool(headers),
            "row_for_reading_only": {k: rec.get(k) for k in ("ok", "refused", "run_args_refused", "run_sha256",
                                                             "script_sha256", "why", "code", "binding_lost")},
            "door_text_for_reading_only": str(scope.get("_data", ""))[:400],
            "error": error,
        }

    out = {"cases": {}, "script_sha256": sha}
    for name in CASES:
        out["cases"][name] = one_case(name)
    # v2.4: taken after the cases, so a module imported lazily during a case (pairstore_excl, A444) is listed too.
    loaded = sorted(os.path.relpath(m.__file__, src) for m in list(sys.modules.values())
                    if getattr(m, "__file__", None) and os.path.abspath(m.__file__).startswith(src + os.sep))
    out["loaded_from_source"] = loaded
    out["unexpected_source_files"] = [f for f in loaded if f not in SOURCE_FILES]
    out["network_events"] = events["net"]
    out["writes_outside_root"] = events["writes_outside"]
    print("PACKET_WORKER_JSON " + json.dumps(out, sort_keys=True))


# ===================================================================== judging (main process)

def expected_for(expected, variant):
    exp = {c: dict(v) for c, v in expected["pinned"].items()}
    for c, over in expected["variants"][variant]["overrides"].items():
        exp[c].update(over)
    return exp


def judge(exp, got):
    """(matches, why). Execution evidence only."""
    diffs = []
    if got["outcome"] not in exp["outcome"]:
        diffs.append("outcome %s, expected %s" % (got["outcome"], "/".join(exp["outcome"])))
    if "reads" in exp and got["reads"] != exp["reads"]:
        diffs.append("%d read(s) of probe.py, expected %d" % (got["reads"], exp["reads"]))
    if "child_args" in exp and got["launches"] and got["child_args"] != exp["child_args"]:
        diffs.append("child arguments %s, expected %s" % (got["child_args"], exp["child_args"]))
    if "planted_loaded" in exp and got.get("planted_loaded") != exp["planted_loaded"]:
        diffs.append("planted json.py loaded: %s, expected %s" % (got.get("planted_loaded"), exp["planted_loaded"]))
    return (not diffs), "; ".join(diffs)


# ===================================================================== main

class SetupError(Exception):
    pass


def fetch_sources(covenant):
    """{file: bytes} for SOURCE_FILES at PIN, plus how they were obtained. Raises SetupError on any problem."""
    covenant = os.path.abspath(covenant)
    files = {}
    genv = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0")
    if os.path.exists(os.path.join(covenant, ".git")):
        how = "git object store of %s (git cat-file blob %s:FILE); the working tree was not read" % (covenant, PIN[:12])
        if not shutil.which("git"):
            raise SetupError("%s is a git clone but git is not on PATH; install git, or pass a folder of the files" % covenant)
        t = subprocess.run(["git", "-C", covenant, "cat-file", "-t", PIN], capture_output=True, text=True, env=genv)
        if t.returncode != 0 or t.stdout.strip() != "commit":
            raise SetupError("the clone at %s does not contain commit %s (fetch it first; README section 3)" % (covenant, PIN))
        for f in SOURCE_FILES:
            r = subprocess.run(["git", "-C", covenant, "cat-file", "blob", "%s:%s" % (PIN, f)], capture_output=True, env=genv)
            if r.returncode != 0:
                raise SetupError("git cat-file failed for %s: %s" % (f, r.stderr.decode(errors="replace").strip()))
            files[f] = r.stdout
    else:
        how = "plain folder %s (files read and checked against the pinned blob hashes)" % covenant
        for f in SOURCE_FILES:
            try:
                with open(os.path.join(covenant, f), "rb") as fh:
                    files[f] = fh.read()
            except OSError as e:
                raise SetupError("cannot read %s in %s (%s); pass the folder that holds covenant_unified_v8.py"
                                 % (f, covenant, type(e).__name__))
    bad = {f: blob_sha(b) for f, b in files.items() if blob_sha(b) != SOURCE_FILES[f]}
    if bad:
        raise SetupError("these files do not match commit %s: %s (a copy with CRLF line endings changes the bytes; "
                         "use a clone, or unpack the zip without converting line endings)" % (PIN, json.dumps(bad)))
    return files, how


def build_variant(files, mutations, dest):
    os.makedirs(dest)
    texts = dict(files)
    for m in mutations:
        f, old, new = MUTATIONS[m]
        s = texts[f].decode("utf-8")
        n = s.count(old)
        if n != 1:
            raise SetupError("break %s: its text occurs %d times in %s, not once; the variant was not built" % (m, n, f))
        texts[f] = s.replace(old, new).encode("utf-8")
    for f, b in texts.items():
        with open(os.path.join(dest, f), "wb") as fh:
            fh.write(b)


def dist_version(name):
    try:
        from importlib.metadata import version
        return version(name)
    except Exception:                     # noqa: BLE001
        return None


def main():
    ap = argparse.ArgumentParser(description="signed-RUN reproduction packet %s (covenant %s)" % (PACKET_VERSION, PIN[:12]))
    ap.add_argument("--covenant", help="a git clone of covenant containing %s, or a folder with the files" % PIN[:12])
    ap.add_argument("--out", help="where to write the record (default: ./signed_run_packet_out_<UTC time>)")
    ap.add_argument("--keep", action="store_true", help="keep the temporary folder (default: delete it at the end)")
    ap.add_argument("--worker", nargs=2, metavar=("SRC", "ROOT"), help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.worker:
        worker(*a.worker)
        return 0
    if not a.covenant:
        ap.error("--covenant PATH is required")

    t0 = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    # v2.2 (DeepSeek): a missing or unreadable expected.json, or an output folder that cannot be made, is exit 2 with a
    # plain message, not a traceback. (No record can be written in the second case: there is nowhere to write it.)
    try:
        with open(os.path.join(here, "expected.json"), "rb") as fh:
            expected_bytes = fh.read()
        expected = json.loads(expected_bytes)
    except (OSError, ValueError) as e:
        print("COULD NOT RUN: expected.json next to run_packet.py is missing or unreadable (%s: %s)" % (type(e).__name__, e))
        return 2
    out_dir = os.path.abspath(a.out or "signed_run_packet_out_%s" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as e:
        print("COULD NOT RUN: cannot create the output folder %s (%s); pass --out to a writable folder" % (out_dir, e))
        return 2
    log_lines, results, worker_raw = [], {}, {}
    with open(os.path.abspath(__file__), "rb") as fh:
        self_sha = hashlib.sha256(fh.read()).hexdigest()
    env = {
        "packet_version": PACKET_VERSION, "covenant_commit": PIN, "covenant_repo": REPO_URL,
        "run_packet_sha256": self_sha, "expected_json_sha256": hashlib.sha256(expected_bytes).hexdigest(),
        "python": sys.version, "python_executable": sys.executable, "platform": platform.platform(),
        "machine": platform.machine(), "flask": dist_version("flask"), "werkzeug": dist_version("werkzeug"),
        "cryptography": dist_version("cryptography"),
        "git": (subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
                if shutil.which("git") else None),
        "command": [sys.executable] + sys.argv, "cwd": os.getcwd(),
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
    }

    def say(s=""):
        print(s, flush=True)
        log_lines.append(s)

    def finish(code, verdict):
        env["seconds"] = round(time.time() - t0, 2)
        env["exit_code"] = code
        say("")
        say("RESULT: %s; %.1f s; exit %d" % (verdict, env["seconds"], code))
        say("record: %s" % out_dir)
        for name, obj in (("environment.json", env), ("results.json", {"exit_code": code, "results": results}),
                          ("workers_raw.json", worker_raw)):
            with open(os.path.join(out_dir, name), "w", encoding="utf-8") as fh:
                json.dump(obj, fh, indent=2, sort_keys=True)
        with open(os.path.join(out_dir, "summary.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(log_lines) + "\n")
        return code

    say("signed-RUN reproduction packet %s -- covenant %s" % (PACKET_VERSION, PIN))
    say("python %s on %s; flask %s, werkzeug %s, cryptography %s" % (sys.version.split()[0], env["platform"], env["flask"],
                                                                       env["werkzeug"], env["cryptography"]))
    say("run_packet.py sha256 %s; expected.json sha256 %s" % (self_sha, env["expected_json_sha256"]))
    if sys.version_info < (3, 10):
        say("Python 3.10 or newer is needed.")
        return finish(2, "COULD NOT RUN")
    missing = [p for p in ("flask", "cryptography") if env[p] is None]
    if missing:
        say("missing package(s): %s -- install them into THIS interpreter: %s -m pip install %s"
            % (", ".join(missing), sys.executable, " ".join(missing)))
        return finish(2, "COULD NOT RUN")
    try:
        files, how = fetch_sources(a.covenant)
    except SetupError as e:
        say("SOURCE CHECK FAILED: %s" % e)
        return finish(2, "COULD NOT RUN")
    env["source"] = how
    say("source: %s; all %d files match their pinned blob hashes" % (how, len(files)))

    tmp = tempfile.mkdtemp(prefix="signed_run_packet_")
    say("temporary folder: %s" % tmp)
    differs = inconclusive = False
    wenv = {k: v for k, v in os.environ.items() if not k.startswith("COVENANT_")}
    wenv["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        for vname, muts in VARIANTS.items():
            vroot = os.path.join(tmp, vname)
            src = os.path.join(vroot, "src")
            try:
                build_variant(files, muts, src)
            except SetupError as e:
                say("VARIANT BUILD FAILED: %s" % e)
                return finish(2, "COULD NOT RUN")
            work = os.path.join(vroot, "work")
            os.makedirs(work)
            cmd = [sys.executable, "-B", os.path.abspath(__file__), "--worker", src, work]
            tv = time.time()
            try:
                cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                    cwd=work, env=wenv, timeout=600)
            except subprocess.TimeoutExpired:
                say("variant %s: the worker did not finish in 600 s" % vname)
                return finish(2, "COULD NOT RUN")
            line = [l for l in cp.stdout.splitlines() if l.startswith("PACKET_WORKER_JSON ")]
            worker_raw[vname] = {"cmd": cmd, "exit": cp.returncode, "stdout": cp.stdout, "stderr": cp.stderr,
                                 "seconds": round(time.time() - tv, 2)}
            if cp.returncode != 0 or not line:
                say("variant %s: the worker failed (exit %s)\n%s" % (vname, cp.returncode, cp.stderr[-3000:]))
                return finish(2, "COULD NOT RUN")
            got = json.loads(line[-1][len("PACKET_WORKER_JSON "):])
            exp = expected_for(expected, vname)
            verdicts = {c: judge(exp[c], got["cases"][c]) for c in CASES}
            met = all(ok for ok, _w in verdicts.values())
            incon = [c for c in CASES if got["cases"][c]["outcome"] == "INCONCLUSIVE"]
            notes = []
            if got["unexpected_source_files"]:
                notes.append("modules loaded from the source folder beyond the pinned list: %s" % got["unexpected_source_files"])
            if got["network_events"]:
                notes.append("network events in the worker: %s" % got["network_events"][:5])
            if got["writes_outside_root"]:
                notes.append("files opened for writing outside the temporary folder: %s" % got["writes_outside_root"][:5])
            met = met and not notes
            differs = differs or not met
            inconclusive = inconclusive or bool(incon)
            results[vname] = {"mutations": muts, "met": met, "inconclusive": incon, "notes": notes,
                              "verdicts": {c: {"matches": ok, "why": w} for c, (ok, w) in verdicts.items()},
                              "expected": exp, "observed": got}
            say("")
            say("variant %-20s %s" % (vname, "AS PRE-REGISTERED" if met else "NOT AS PRE-REGISTERED"))
            for c in CASES:
                ok, why = verdicts[c]
                o = got["cases"][c]
                say("  %-31s %-5s %-16s reads=%d launches=%d args=%s%s" % (
                    c, "ok" if ok else "DIFF", o["outcome"], o["reads"], o["launches"],
                    o["child_args"] if o["launches"] else "-", ("  <- " + why) if why else ""))
                if o["inconclusive_why"]:
                    say("      inconclusive: %s" % "; ".join(o["inconclusive_why"]))
            for n in notes:
                say("  NOTE: %s" % n)
    finally:
        if a.keep:
            say("kept: %s" % tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
            say("removed the temporary folder")

    n_met = sum(1 for r in results.values() if r["met"])
    if inconclusive:
        return finish(3, "INCONCLUSIVE -- a fixture did not do its part; %d of %d variants as pre-registered" % (n_met, len(VARIANTS)))
    if differs:
        return finish(1, "DIFFERS FROM THE PRE-REGISTRATION -- %d of %d variants as pre-registered" % (n_met, len(VARIANTS)))
    return finish(0, "ALL AS PRE-REGISTERED -- %d of %d variants" % (n_met, len(VARIANTS)))


if __name__ == "__main__":
    sys.exit(main())
