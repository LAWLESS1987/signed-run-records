# The claim this packet checks, read against the source (packet v2.4)

Covenant commit `ead187b2513fba7bce1404cf3678ae128f38b1b8` (public `main` of
https://github.com/LAWLESS1987/covenant, 2026-11-18). Line numbers below are at that commit.
Checked by Claude (an AI) on 2026-11-18 by reading the code and running the packet. ChatGPT reviewed v1 of this
reading. Its corrections are folded in here and marked (R). v2.3's reading, of commit `9d85f6c`, is kept in the
gist's history and in `CHANGES.md`; what changed between the two commits is said where it matters.

## As posted publicly (HF 180706 #36 and 183807 #42, 2026-11-17)

At a pinned commit, not a deployed system:
1. the operator's signed request names the script by the SHA-256 of the script file's bytes, and a script whose bytes
   don't match is refused;
2. a signed run that carries arguments is refused;
3. an unsigned run is refused.

The hash covers that one file, not anything it imports. Screening is a separate deny-list check and is not part of
the claim. The source reads the bytes once and never reopens the file.

## What the code does, in the order it does it

**The door** (`covenant_unified_v8.py`, the `/m/agent` route's HANDS branch, lines 9518-9640):
1. `_may_run = _request_signed_by_registered(request)` (line 9530). That function (lines 559-573) calls
   `covenant_mycelium.admit` with the address check forced off, and returns true only when `admit` reports
   `signed:operator`. The caller's address never grants a run, loopback included (A423), and an ally key does not
   either (A447; at `9d85f6c` it did, case C1).
2. `admit` (`covenant_mycelium.py` lines 114-167) accepts a request in two ways **(R)**, and only the first can
   authorize a run:
   - **An operator signer.** `covenant_daily_plan.verify_signed` (`covenant_daily_plan.py` lines 357-385) checks that
     the public key is in the signer registry, the timestamp is finite and within 300 s, and the signature verifies:
     RSA PSS SHA-256 over a domain-framed message of the public key, method, path, sha256 of the exact body bytes,
     nonce and timestamp (`covenant_unified_v8.py` lines 1966-2014). The nonce is then checked and recorded once in a
     durable store shared by the processes of one checkout (`nonce_check_and_record`, lines 95-123; A444): one file per
     (signer, nonce), made with a link that fails if the file already exists. At `9d85f6c` it was an in-memory set
     that emptied on restart **(R)**. The source says replay against a second host is not closed by it. The packet
     points the store into its temporary folder. The packet's throwaway keys are RSA-2048
     because `sig_keygen` makes them so; the verifier itself does not check key size **(R)**.
   - **An ally.** If the key is not an operator signer but is registered as an ally, and the path is in that ally's
     scope (the default scope includes `/m/agent`), the same signature, window and nonce checks admit it as
     `signed:ally`. That is no longer enough for a RUN (step 1). Case C1 is pre-registered as refused.
3. Only when `_may_run` is true is `run_sha256` read from the JSON body (line 9537). The door always passes
   `run_sha256` to the hands (None when there is none), so on this path a run is always bound.

**The hands** (`covenant_tetsu_hands.py`, `act()` lines 914-1065), in order **(R)**:
1. `parse` (lines 689-703) takes the target and the arguments from the model's answer line.
2. `_capture` (lines 764-783) checks the name is a workshop name and that the file's real location is inside the
   workshop, then reads the file once (at most MAX_FILE + 1 bytes).
3. The shared quorum is asked (stubbed in the packet), and the content seat screens the captured bytes.
4. Without `may_run`: refused, and no process is started (line 988). The text handed to the model is
   `RUN_REFUSED_DATA` (line 909; A446): a run needs a request signed by one of the operator's own registered keys,
   and loopback alone, an ally key or a tailnet address is not enough. The file has already been read once, the gate
   asked and a ledger row written. **"Refused" here means no launch, not "nothing happened" (R).**
5. A bound (signed-door) run with any arguments: refused, no process started (A436, line 1008).
6. `run()` (lines 501-546) hashes the captured bytes (line 519), and refuses when the hash is not the signed
   `run_sha256`, or there is none, or it is not 64 lowercase hex characters (`_binding_refusal`, lines 488-498). It
   screens the same bytes (line 526) and starts the child as `python -I -c RUNNER <workshop> <name>` with the
   workshop as its working directory (line 536), handing it the bytes on standard input. RUNNER (lines
   246-261) reads its code from standard input (line 249) and executes it (line 260). `-I` keeps the
   working directory off the child's `sys.path`, so a file planted beside the script (case 10) is not imported in its
   place.

**One thing on the path that is not the claim's.** Importing the core runs `_imports_fingerprint()` (line 501),
which imports `covenant_watchdog`; its line 72 calls `covenant_quiet.install()` (`covenant_quiet.py` lines
164-173). That replaces `subprocess.Popen.__init__` for the whole process. Off Windows it changes nothing; on Windows it
adds a no-window flag and swaps a `pythonw` program for its console twin (lines 118-127), then calls the original
`__init__`, which raises the audit event the packet reads. Found by nootxlm in v2.3; the README now says it.

## What the packet measures, and what stays a reading of the source

Measured, by execution (marker files; launches and their arguments from the `subprocess.Popen` audit event; the
parent's opens of the script from the `open` audit event):
- a signed run with no arguments runs the approved bytes (1, 5a, 5b), with no child arguments;
- changed bytes (2) and a one-byte change (2b) are refused, with no launch;
- one argument (3b) and two (3) are refused, with no launch;
- unsigned from loopback (4) and from a tailnet address (4b) are refused, with no launch;
- the signature is bound to the body: a body changed after signing (6) and a bad signature by the registered key (7)
  are refused; so are a valid signature by an unregistered key (8) and a signed body without `run_sha256` (9);
- **in the parent, the script file is opened exactly once** while the door handles the request, in every case. The
  `extra_parent_read` break shows the count can see a second read;
- **the child runs the parent's bytes, not the file**: replaced at the launch (5a), or continuously from the gate
  (5b), the substitute never ran on the pinned code, and the `child_reopens` break shows it would have;
- **a planted `json.py` beside the script is not imported** (10), and the `no_isolation` break (no `-I`) shows the
  case can see it if it is;
- C1 (characterization): an ally key with the default scope is refused, with no launch; the `no_signature_check`,
  `no_registry_check` and `accept_everything` breaks show the case can see it run.

A reading of the source, not measured: what the child does with standard input beyond these cases (the child is not
audited); the content seat being shown the same bytes (covenant's own `test_a430_run_sha256.py` covers it); what the
approved script does to its own `sys.path` once it runs; every other way in through the route. Each of the eleven
broken copies is one specific way to be wrong. None of them shows that there is no other way.

## How the packet reaches the code, and what that leaves out

As covenant's own `test_a430_run_sha256.py` does, the packet takes the one `if first.upper().startswith('HANDS')`
block from the parsed core and executes it in a Flask test request context. It uses real signatures, the real
hands module, real child processes and the real screen. Stubbed: the model (its answer line is fixed per case) and
the shared quorum (always "clean").

Not run: the rest of the `/m/agent` route (the model call, the act-word guard A427, the private branch), any HTTP
socket, a deployed node, the phone's signer, runtime containment and egress, key theft and revocation, replay across a
restart or a second process (A444's own test covers it), and the owner's in-process paths (the practice loop and
`--run` at the console). Those paths run without a signature by design (KNOWN_ISSUES A430, "Not bound by this"; A434).
