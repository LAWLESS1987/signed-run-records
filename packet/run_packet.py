#!/usr/bin/env python3
"""Signed-RUN reproduction packet, v1 (Mutual Benefit Collective issue #21).

ONE COMMAND
    python run_packet.py --covenant PATH

PATH is either a git clone of https://github.com/LAWLESS1987/covenant that contains the pinned commit below, or a
folder holding the eight covenant files listed in SOURCE_FILES (for example an unpacked GitHub zip of that commit).
Every file taken from PATH must match the git blob hash recorded below, or nothing runs (exit 2).

WHAT IT DOES
  * Copies the eight pinned covenant files (from the git object database when PATH is a clone, never the working
    tree) into a new temporary folder. The clone or folder you point at is only read, never written.
  * For each of seven VARIANTS (the pinned code, and six deliberately broken copies of it) it starts one fresh
    Python process (the worker) that runs the five cases in expected.json against that variant's copy.
  * Each case uses its own temporary workshop. The scripts under test write a marker file when they run; the worker
    counts the child processes the hands start with an audit hook. Only those two things decide a case.
  * Prints a table, writes the raw record to an output folder, and exits 0 only when every variant fails exactly
    the cases expected.json says it must, and passes the rest.

WHAT IT NEEDS
  Python 3.10 or newer, and the packages flask and cryptography (the covenant core imports both). git only when
  PATH is a clone. No network, no account, no key of ours: the signing key is an RSA key generated in memory for the
  run and its public half is registered in a temporary file.

WHAT IT DOES NOT TEST -- read README.md. In short: one door path at one commit, with the model and the judges stubbed;
not a deployed node, not runtime containment, not the screen, not key theft.
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import threading
import time

PACKET_VERSION = "v1"
PIN = "9d85f6c902bcfab4616be0d3b08d0715584f7a07"
REPO_URL = "https://github.com/LAWLESS1987/covenant"

# git blob hashes of the files at PIN (git rev-parse PIN:FILE). These eight are every covenant module the worker
# imports, measured with an audit hook when the packet was built; the worker checks again at run time that no other
# file from the source folder was loaded.
SOURCE_FILES = {
    "covenant_daily_plan.py": "45d37b67229b98545d329eb3fce4c45f1c3e7052",
    "covenant_mycelium.py": "d43a9a40c0213207c8162aadb705c29ce20468ae",
    "covenant_path_pattern.py": "ff394e611747a054e3707970dbf06745dd02b885",
    "covenant_quiet.py": "87eebf68fef95c3ab1ebf4c3d45191db74961c02",
    "covenant_semantic_judge.py": "20f6b67cee9f7657109011d16613e025476b9915",
    "covenant_tetsu_hands.py": "e5301d038f4649e6b8d80c939e861b3bba967689",
    "covenant_unified_v8.py": "70a0dc97188648f0bd735f2d369671dd661c5f11",
    "covenant_watchdog.py": "bad40ce5f46cbae3d889efadfe37ecbc1224d5f6",
}

# The deliberate breaks. Each is an exact text replacement in the temporary copy; each text must occur exactly once
# in its file, or the run stops (exit 2) rather than test a variant that was not built.
_BIND_DOC = 'None when the bytes about to run hash to the approved run_sha256; else why the run is refused."""'
MUTATIONS = {
    "no_signature_check": ("covenant_unified_v8.py", "_may_run = _request_signed_by_registered(request)",
                           "_may_run = True"),
    "no_hash_check": ("covenant_tetsu_hands.py", _BIND_DOC, _BIND_DOC + "\n    return None"),
    "always_refuse": ("covenant_tetsu_hands.py", _BIND_DOC, _BIND_DOC + "\n    return 'always-refuse variant'"),
    "no_args_check": ("covenant_tetsu_hands.py", 'if run_sha256 is not UNBOUND and d["args"]:', "if False:"),
    "child_reopens": ("covenant_tetsu_hands.py", "code = sys.stdin.buffer.read()",
                      'code = open(os.path.join(WS, script), "rb").read()'),
}
VARIANTS = {
    "pinned": [],
    "always_refuse": ["always_refuse"],
    "accept_everything": ["no_signature_check", "no_hash_check", "no_args_check", "child_reopens"],
    "no_signature_check": ["no_signature_check"],
    "no_hash_check": ["no_hash_check"],
    "no_args_check": ["no_args_check"],
    "child_reopens": ["child_reopens"],
}

# The scripts under test. Each writes its own marker inside the workshop (the hands allow a script to open files only
# there) and prints one line. sha256(APPROVED) is what the operator signs.
SCRIPTS = {
    "approved": b'with open("ran_approved.txt", "w") as fh:\n    fh.write("approved")\nprint("approved bytes ran")\n',
    "changed": b'with open("ran_changed.txt", "w") as fh:\n    fh.write("changed")\nprint("changed bytes ran")\n',
    "substitute": b'with open("ran_substitute.txt", "w") as fh:\n    fh.write("substitute")\nprint("substitute bytes ran")\n',
}
CASES = ["1_signed_no_args", "2_changed_bytes", "3_added_args", "4_unsigned", "5a_swap_at_launch", "5b_swap_continuous"]


def blob_sha(data):
    """git's blob hash of these bytes (what `git hash-object` prints)."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


# ===================================================================== worker (one variant, one fresh process)

def worker(src, root):
    """Run the cases against the covenant files in `src`; print one JSON line. Everything it writes is under root."""
    src, root = os.path.abspath(src), os.path.abspath(root)
    sys.dont_write_bytecode = True
    events = {"popen": [], "net": [], "writes_outside": []}

    def audit(ev, args):
        if ev == "subprocess.Popen":
            events["popen"].append([str(a) for a in (args[1] if len(args) > 1 and isinstance(args[1], (list, tuple)) else [args[0]])][:6])
        elif ev.startswith("socket."):
            events["net"].append([ev, repr(args)[:160]])
        elif ev == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else 0
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or \
                (isinstance(flags, int) and bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT)))
            if writing:
                p = os.path.abspath(os.fsdecode(args[0]))
                if not (p == root or p.startswith(root + os.sep)):
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
    sys.path.insert(0, src)

    import ast
    import importlib
    from unittest.mock import patch
    from flask import Flask, request
    import covenant_daily_plan as DP
    import covenant_mycelium as MY
    import covenant_tetsu_hands as H
    import covenant_unified_v8 as cov

    loaded = sorted(os.path.relpath(m.__file__, src) for m in list(sys.modules.values())
                    if getattr(m, "__file__", None) and os.path.abspath(m.__file__).startswith(src + os.sep))
    unexpected = [f for f in loaded if f not in SOURCE_FILES]

    # The door's real HANDS branch, taken from this variant's core file exactly as covenant's own test_a430_run_sha256
    # does (the one `if first.upper().startswith('HANDS')` block), and executed in a Flask request context.
    tree = ast.parse(open(cov.__file__, encoding="utf-8").read())
    found = [n for n in ast.walk(tree) if isinstance(n, ast.If) and ast.unparse(n.test) == "first.upper().startswith('HANDS')"]
    if len(found) != 1:
        raise SystemExit("expected exactly one HANDS branch in the core, found %d" % len(found))
    branch = compile(ast.Module(body=found[0].body, type_ignores=[]), cov.__file__, "exec")

    key, pem = cov.sig_keygen()          # throwaway RSA-2048 key, in memory only; its public half is registered below
    app = Flask("signed_run_packet")
    approved_sha = hashlib.sha256(SCRIPTS["approved"]).hexdigest()

    def one_case(name):
        case = os.path.join(root, name)
        shop = os.path.join(case, "workshop")
        os.makedirs(shop)
        signers = os.path.join(case, "signers.json")
        with open(signers, "w", encoding="utf-8") as fh:
            json.dump({"packet-throwaway": pem}, fh)
        probe = os.path.join(shop, "probe.py")
        with open(probe, "wb") as fh:
            fh.write(SCRIPTS["changed" if name == "2_changed_bytes" else "approved"])
        answer = "HANDS RUN probe.py --extra 1" if name == "3_added_args" else "HANDS RUN probe.py"
        signed = name != "4_unsigned"
        body = json.dumps({"run_sha256": approved_sha}).encode("utf-8")
        headers = cov.sign_operator_request(key, pem, "POST", "/m/agent", body) if signed else {}
        swap = {"writes": 0, "errors": 0}
        stop = threading.Event()
        threads = []

        def write_substitute():
            tmp = probe + ".swap"
            with open(tmp, "wb") as fh:
                fh.write(SCRIPTS["substitute"])
            os.replace(tmp, probe)
            swap["writes"] += 1

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
            return "clean", "packet fixture: quorum stubbed"

        real_run = H.subprocess.run

        def swap_then_launch(*a, **k):    # 5a: after the hash check and the screen, at the launch itself
            write_substitute()
            return real_run(*a, **k)

        patches = [patch.object(H, "WORKSHOP", shop), patch.object(H, "LEDGER", os.path.join(case, "hands.jsonl")),
                   patch.object(H, "_gate", gate), patch.object(DP, "SIGNERS", signers),
                   patch.object(DP, "_seen_nonces", set()),
                   patch.object(MY, "PEERS", os.path.join(case, "no_allies.json")),
                   patch.object(MY, "LEDGER", os.path.join(case, "mycelium.jsonl"))]
        if name == "5a_swap_at_launch":
            patches.append(patch.object(H.subprocess, "run", swap_then_launch))
        popen_before = len(events["popen"])
        scope = {"request": request, "answer": answer, "importlib": importlib,
                 "_request_signed_by_registered": cov._request_signed_by_registered,
                 "forum": [], "msgs": [], "_ask_fitted": lambda: ("done", {})}
        error = None
        for p in patches:
            p.start()
        try:
            with app.test_request_context("/m/agent", method="POST", data=body, headers=headers,
                                          content_type="application/json"):
                exec(branch, scope)
        except Exception as e:            # noqa: BLE001 -- recorded, and the markers still decide
            error = "%s: %s" % (type(e).__name__, str(e)[:300])
        finally:
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
        disk = [k for k, v in SCRIPTS.items() if v == on_disk] or ["other"]
        rec = scope.get("_rec") or {}
        return {
            "markers": markers,
            "child_processes": len(events["popen"]) - popen_before,
            "child_argv_head": [e[:3] for e in events["popen"][popen_before:]],
            "probe_on_disk_after": disk[0],
            "swap_writes": swap["writes"], "swap_errors": swap["errors"],
            "answer": answer, "signed": signed,
            "row_for_reading_only": {k: rec.get(k) for k in ("ok", "refused", "run_args_refused", "run_sha256",
                                                             "script_sha256", "why", "code", "binding_lost")},
            "door_text_for_reading_only": str(scope.get("_data", ""))[:400],
            "error": error,
        }

    out = {"cases": {}, "loaded_from_source": loaded, "unexpected_source_files": unexpected,
           "approved_sha256": approved_sha}
    for name in CASES:
        out["cases"][name] = one_case(name)
    out["network_events"] = events["net"]
    out["writes_outside_root"] = events["writes_outside"]
    print("PACKET_WORKER_JSON " + json.dumps(out, sort_keys=True))


# ===================================================================== judging a case (main process)

def judge(name, exp, got):
    """(passed, reason). Execution evidence only: markers and child-process counts."""
    if got.get("error"):
        # an exception is recorded; it decides nothing by itself -- the markers below still do
        pass
    ran = set(got["markers"])
    forbidden = [w for w in exp.get("must_not_ran", []) if w in ran]
    if forbidden:
        return False, "ran: %s" % ", ".join(forbidden)
    if name.startswith("5"):
        if "approved" in ran and got["child_processes"] == 1:
            if got["probe_on_disk_after"] != "substitute":
                return False, "the swap did not happen (probe.py on disk is %s), so the case tested nothing" % got["probe_on_disk_after"]
            return True, "approved ran in 1 child; the file on disk had been swapped"
        if not ran and got["child_processes"] == 0:
            return True, "nothing ran and no child started"
        return False, "markers %s with %d child process(es)" % (sorted(ran) or "none", got["child_processes"])
    missing = [w for w in exp.get("must_ran", []) if w not in ran or got["markers"].get(w) != w]
    if missing:
        return False, "did not run: %s" % ", ".join(missing)
    if got["child_processes"] != exp["child_processes"]:
        return False, "%d child process(es), expected %d" % (got["child_processes"], exp["child_processes"])
    return True, ("ran" if exp.get("must_ran") else "refused: nothing ran, no child started")


# ===================================================================== main

def fetch_sources(covenant):
    """{file: bytes} for SOURCE_FILES at PIN, plus how they were obtained. Raises SystemExit(2) on any mismatch."""
    covenant = os.path.abspath(covenant)
    files, how = {}, None
    if os.path.exists(os.path.join(covenant, ".git")):
        how = "git object database of %s (git cat-file blob %s:FILE); the working tree was not read" % (covenant, PIN[:12])
        t = subprocess.run(["git", "-C", covenant, "cat-file", "-t", PIN], capture_output=True, text=True)
        if t.returncode != 0 or t.stdout.strip() != "commit":
            raise SystemExit("the clone at %s does not contain commit %s (git fetch it first)" % (covenant, PIN))
        for f in SOURCE_FILES:
            r = subprocess.run(["git", "-C", covenant, "cat-file", "blob", "%s:%s" % (PIN, f)], capture_output=True)
            if r.returncode != 0:
                raise SystemExit("git cat-file failed for %s: %s" % (f, r.stderr.decode(errors="replace")))
            files[f] = r.stdout
    else:
        how = "plain folder %s (files read and checked against the pinned blob hashes)" % covenant
        for f in SOURCE_FILES:
            with open(os.path.join(covenant, f), "rb") as fh:
                files[f] = fh.read()
    bad = {f: blob_sha(b) for f, b in files.items() if blob_sha(b) != SOURCE_FILES[f]}
    if bad:
        raise SystemExit("these files do not match commit %s: %s (a CRLF checkout of a zip changes the bytes; use a "
                         "clone, or a zip with LF endings)" % (PIN, json.dumps(bad)))
    return files, how


def build_variant(files, mutations, dest):
    os.makedirs(dest)
    texts = dict(files)
    for m in mutations:
        f, old, new = MUTATIONS[m]
        s = texts[f].decode("utf-8")
        n = s.count(old)
        if n != 1:
            raise SystemExit("mutation %s: its text occurs %d times in %s, not once; the variant was not built" % (m, n, f))
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
    ap.add_argument("--covenant", required=False, help="a git clone of covenant containing %s, or a folder with the files" % PIN[:12])
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
    with open(os.path.join(here, "expected.json"), "rb") as fh:
        expected_bytes = fh.read()
    expected = json.loads(expected_bytes)
    out_dir = os.path.abspath(a.out or "signed_run_packet_out_%s" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
    os.makedirs(out_dir, exist_ok=True)
    log_lines = []

    def say(s=""):
        print(s, flush=True)
        log_lines.append(s)

    env = {
        "packet_version": PACKET_VERSION, "covenant_commit": PIN, "covenant_repo": REPO_URL,
        "run_packet_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(),
        "expected_json_sha256": hashlib.sha256(expected_bytes).hexdigest(),
        "python": sys.version, "python_executable": sys.executable, "platform": platform.platform(),
        "machine": platform.machine(), "flask": dist_version("flask"), "werkzeug": dist_version("werkzeug"),
        "cryptography": dist_version("cryptography"),
        "git": (subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
                if shutil.which("git") else None),
        "command": [sys.executable] + sys.argv,
        "cwd": os.getcwd(),
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
    }
    say("signed-RUN reproduction packet %s -- covenant %s" % (PACKET_VERSION, PIN))
    say("python %s on %s; flask %s, werkzeug %s, cryptography %s" % (sys.version.split()[0], env["platform"], env["flask"],
                                                                       env["werkzeug"], env["cryptography"]))
    say("expected.json sha256 %s" % env["expected_json_sha256"])
    if sys.version_info < (3, 10):
        say("Python 3.10 or newer is needed.")
        return 2
    missing = [p for p in ("flask", "cryptography") if env[p] is None]
    if missing:
        say("missing package(s): %s -- pip install %s" % (", ".join(missing), " ".join(missing)))
        return 2
    try:
        files, how = fetch_sources(a.covenant)
    except SystemExit as e:
        say("SOURCE CHECK FAILED: %s" % e)
        return 2
    env["source"] = how
    say("source: %s; all %d files match their pinned blob hashes" % (how, len(files)))

    tmp = tempfile.mkdtemp(prefix="signed_run_packet_")
    say("temporary folder: %s" % tmp)
    results, worker_raw = {}, {}
    all_met = True
    wenv = {k: v for k, v in os.environ.items() if not k.startswith("COVENANT_")}
    wenv["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        for vname, muts in VARIANTS.items():
            vroot = os.path.join(tmp, vname)
            src = os.path.join(vroot, "src")
            try:
                build_variant(files, muts, src)
            except SystemExit as e:
                say("VARIANT BUILD FAILED: %s" % e)
                return 2
            work = os.path.join(vroot, "work")
            os.makedirs(work)
            cmd = [sys.executable, "-B", os.path.abspath(__file__), "--worker", src, work]
            tv = time.time()
            cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                cwd=work, env=wenv, timeout=600)
            line = [l for l in cp.stdout.splitlines() if l.startswith("PACKET_WORKER_JSON ")]
            worker_raw[vname] = {"cmd": cmd, "exit": cp.returncode, "stdout": cp.stdout, "stderr": cp.stderr,
                                 "seconds": round(time.time() - tv, 2)}
            if cp.returncode != 0 or not line:
                say("variant %s: the worker failed (exit %s)\n%s" % (vname, cp.returncode, cp.stderr[-3000:]))
                return 2
            got = json.loads(line[-1][len("PACKET_WORKER_JSON "):])
            verdicts = {c: judge(c, expected["cases"][c], got["cases"][c]) for c in CASES}
            failed = sorted(c for c, (ok, _w) in verdicts.items() if not ok)
            must_fail = sorted(expected["variants"][vname]["must_fail"])
            met = failed == must_fail
            all_met = all_met and met
            results[vname] = {"mutations": muts, "failed": failed, "must_fail": must_fail, "met": met,
                              "verdicts": {c: {"passed": ok, "why": w} for c, (ok, w) in verdicts.items()},
                              "observed": got}
            say("")
            say("variant %-19s %s  (fails %s; pre-registered to fail %s)" % (
                vname, "AS PRE-REGISTERED" if met else "NOT AS PRE-REGISTERED", failed or "none", must_fail or "none"))
            for c in CASES:
                ok, why = verdicts[c]
                o = got["cases"][c]
                say("  %-20s %s  %s | markers=%s children=%d disk_after=%s" % (
                    c, "pass" if ok else "FAIL", why, sorted(o["markers"]) or "none", o["child_processes"],
                    o["probe_on_disk_after"]))
            if got["unexpected_source_files"]:
                say("  NOTE: modules loaded from the source folder beyond the pinned list: %s" % got["unexpected_source_files"])
                all_met = False
            if got["network_events"]:
                say("  NOTE: network events in the worker: %s" % got["network_events"][:5])
                all_met = False
            if got["writes_outside_root"]:
                say("  NOTE: files opened for writing outside the temporary folder: %s" % got["writes_outside_root"][:5])
                all_met = False
            if vname == "pinned":
                for c in ("5a_swap_at_launch", "5b_swap_continuous"):
                    detail = "approved_ran" if "approved" in got["cases"][c]["markers"] else "nothing_ran"
                    pre = expected["cases"][c].get("pinned_expected_detail")
                    say("  %s on the pinned code: %s (pre-registered: %s)" % (c, detail, pre))
    finally:
        if a.keep:
            say("kept: %s" % tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
            say("removed the temporary folder")

    secs = round(time.time() - t0, 2)
    env["seconds"] = secs
    code = 0 if all_met else 1
    say("")
    say("RESULT: %s -- %d of %d variants as pre-registered; %.1f s; exit %d" % (
        "ALL AS PRE-REGISTERED" if all_met else "DIFFERS FROM THE PRE-REGISTRATION",
        sum(1 for r in results.values() if r["met"]), len(VARIANTS), secs, code))
    say("record: %s" % out_dir)
    with open(os.path.join(out_dir, "environment.json"), "w", encoding="utf-8") as fh:
        json.dump(env, fh, indent=2)
    with open(os.path.join(out_dir, "results.json"), "w", encoding="utf-8") as fh:
        json.dump({"exit_code": code, "results": results}, fh, indent=2, sort_keys=True)
    with open(os.path.join(out_dir, "workers_raw.json"), "w", encoding="utf-8") as fh:
        json.dump(worker_raw, fh, indent=2)
    with open(os.path.join(out_dir, "summary.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log_lines) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
