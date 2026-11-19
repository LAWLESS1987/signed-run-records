# The claim this packet checks, read against the source (packet v1)

Covenant commit `9d85f6c902bcfab4616be0d3b08d0715584f7a07` (public `main` of
https://github.com/LAWLESS1987/covenant, 2026-11-16). Line numbers below are at that commit.
Checked by Claude (an AI) on 2026-11-17 by reading the code and by running the packet.

## As posted publicly (HF 180706 #36 and 183807 #42, 2026-11-17)

At a pinned commit, not a deployed system:
1. the operator's signed request names the script by the SHA-256 of the script file's bytes, and a script whose bytes
   don't match is refused;
2. a signed run that carries arguments is refused;
3. an unsigned run is refused.

The hash covers that one file, not anything it imports. Screening is a separate deny-list check and is not part of
the claim. Our source also reads the bytes once and never reopens the file (case 5 tests this).

## What the code does

**The door** (`covenant_unified_v8.py`, the `/m/agent` route's HANDS branch, from line 9491):
- `_may_run = _request_signed_by_registered(request)` (line 9503). That function (line 559) calls
  `covenant_mycelium.admit` with the address check forced off, so the caller's address never grants a run, loopback
  included (A423).
- `admit` (`covenant_mycelium.py` line 114) hands the `X-Operator-*` headers to `covenant_daily_plan.verify_signed`
  (`covenant_daily_plan.py` line 300): the public key must be in the signer registry, the timestamp finite and within
  300 s, the nonce unseen, and the RSA-2048 PSS SHA-256 signature must verify over a domain-framed message of the
  public key, method, path, sha256 of the exact body bytes, nonce and timestamp (`covenant_unified_v8.py` lines
  1960-2009).
- Only when the signature verified is `run_sha256` read from the JSON body (line 9510). Then
  `covenant_tetsu_hands.act(answer, may_run=..., run_sha256=...)` (line 9511). The door always passes `run_sha256`
  (None when there is none), so on this path a run is always bound.

**The hands** (`covenant_tetsu_hands.py`):
- `act()` (line 905) reads the RUN's script once, before anything else (`_capture`, line 924; at most MAX_FILE + 1
  bytes; a name outside the workshop or a link out of it is not opened).
- No signature: refused before anything starts (line 975).
- A signed run with any arguments: refused before anything starts (A436, line 999).
- `run()` (line 501) takes the captured bytes (line 513), hashes them (line 519), refuses when the hash is not the
  signed `run_sha256`, or there is none, or it is not 64 lowercase hex characters (`_binding_refusal`, line 488),
  screens the same bytes (line 526), and gives them to the child on standard input (line 537). The child is
  `python -I -c RUNNER` (RUNNER from line 246), which reads its code from standard input (line 249) and executes it
  (line 260). Nothing reopens the file.

## Verdict: the code supports the claim as posted, with these precisions

None of them narrows what the posts said; they say exactly what each word means here.

- **"Signed"** means signed by a key in the node's signer registry, fresh (300 s), single-use nonce, over the exact
  body bytes. In the source, a valid signature by an unregistered key is refused (`verify_signed` returns "key is not
  a registered daily-plan signer"). Neither this packet nor the four covenant tests named in the README has a case
  for it; that part is a reading of the source.
- **"Unsigned run is refused"** is a property of the `/m/agent` door. `act()` itself defaults to `may_run=True`. Its
  in-process callers, the owner-started practice loop (bounded separately by A434) and
  `python covenant_tetsu_hands.py --run` at the console, run without a signature by design (KNOWN_ISSUES A430, "Not
  bound by this").
- **"Arguments refused"** applies to a signed door run with any argument at all. There is no way to sign arguments:
  a signed run runs with none (A436's stated cost).
- **"The hash covers that one file"**: the bytes of the entry script only. It does not cover the Python interpreter
  or the standard-library modules the script imports. The screen limits imports to a fixed allowlist, and screening
  is not part of this claim.
- **"Reads once"**: the parent reads once and the child gets the bytes on standard input. Case 5 swaps the file
  after that read, at the launch itself (5a) and continuously from the gate until the act returns (5b). The content
  seat being shown the same bytes is covered by covenant's own test, not by this packet.

## How the packet reaches the code, and what that leaves out

The packet runs the door's real HANDS branch the same way covenant's own `test_a430_run_sha256.py` does: it parses
`covenant_unified_v8.py`, takes the one `if first.upper().startswith('HANDS')` block from the syntax tree, and
executes it in a Flask test request context, with real signatures, the real hands module, real child processes
and the real screen. Stubbed: the model (its answer line is fixed per case) and the shared quorum (always "clean",
so only the binding logic decides).

Not run: the rest of the `/m/agent` route (the model call, the act-word guard A427 and the private branch that sit
before the HANDS branch), any HTTP socket, a deployed node, the phone's signer, runtime containment and egress, key
theft and revocation.
