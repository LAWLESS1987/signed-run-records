# Signed-RUN reproduction packet, v1

One narrow rule in covenant's source, checked by one command on your own machine:

> At covenant commit `9d85f6c902bcfab4616be0d3b08d0715584f7a07`, not a deployed system: the operator's signed request
> names the script by the SHA-256 of the script file's bytes, and a script whose bytes don't match is refused; a
> signed run that carries arguments is refused; an unsigned run is refused. The bytes are read once and never
> reopened.

`CLAIM.md` has that claim read against the source, line by line, with what each word means and what is left out.
Passing these cases would not show that covenant is secure, contained or deployed. It would show only that this one
rule held on your machine for these cases.

Written by Claude (an AI) for the Mutual Benefit Collective, issue #21, at Lawrence's direction. Our own
runs are **internal preparation**, kept apart under `../runs/`. A run on your machine is the outside reproduction,
and it is yours: you report what you saw, including anything that differs from ours.

## 1. Read it first

Please read everything before you run it. A VM or container is fine; you need nothing of ours inside it.

**The packet itself** is three files: `run_packet.py` (482 lines, the only code), `expected.json` (the outcomes we
committed before our first run), and this README. `CLAIM.md` and `REVIEWER_RETURN.md` are text.

**The covenant code under test is not small.** The eight files the packet imports total 20,751 lines, 14,050 of them
in `covenant_unified_v8.py`, the node's core. The part these cases actually exercise is short. At the pinned commit:

| file | lines | what |
|---|---|---|
| `covenant_unified_v8.py` | 9491-9516 | the `/m/agent` door's HANDS branch: who may run, and where `run_sha256` comes from |
| `covenant_unified_v8.py` | 559-567 | `_request_signed_by_registered`: the address never grants a run |
| `covenant_unified_v8.py` | 1945-2009 | key generation, the signed message, signing and verifying (RSA-2048, PSS, SHA-256) |
| `covenant_mycelium.py` | 114-166 | `admit`: the signature headers handed to the verifier |
| `covenant_daily_plan.py` | 300-326 | `verify_signed`: registered key, 300 s window, single-use nonce |
| `covenant_tetsu_hands.py` | 246-261 | RUNNER: the child reads its code from standard input |
| `covenant_tetsu_hands.py` | 488-546 | `_binding_refusal` and `run()`: hash, screen and launch the same bytes |
| `covenant_tetsu_hands.py` | 689-703, 764-799 | `parse` (where arguments come from), `_capture` and `_captured` (the single read) |
| `covenant_tetsu_hands.py` | 905-1033 | `act()`: the order of the refusals |

The other five files (`covenant_path_pattern.py`, `covenant_quiet.py`, `covenant_semantic_judge.py`,
`covenant_watchdog.py`, and the rest of the core) are loaded because the core imports them. With the packet's
eight files only, `covenant_semantic_judge` prints a warning that it has no model file. That is expected, and the
judge is not used.

**What the packet does on your machine:**
- It reads the eight files at the pinned commit, with `git cat-file` from your clone's object store (the working tree
  is not read), or from a plain folder, and checks each against its git blob hash. On any mismatch it stops with
  exit 2 before running anything.
- It makes one temporary folder (Python's `tempfile`, prefix `signed_run_packet_`). It writes there and into the
  output folder, and nowhere else. It deletes the temporary folder at the end unless you pass `--keep`.
- It starts one worker Python process per variant (seven), and each worker starts child Python processes that run the
  three tiny scripts printed in `run_packet.py` (`SCRIPTS`). Each script writes one marker file inside its
  temporary workshop and prints one line. That is all any script under test does.
- It generates an RSA key in memory for each worker and registers only its public half, in a temporary file. No key
  of ours is involved.
- Network: none is needed. Each worker installs a Python audit hook before importing covenant. It records every
  socket event, every child process and every file opened for writing outside the temporary folder, and the run
  reports any it saw. On our runs it saw no socket events and no writes outside. The main process is not audited.
  It runs `git` locally and starts the workers. Fetching the commit (step 3) needs the network once; the run does not.

## 2. What you need

- Python 3.10 or newer.
- `pip install flask cryptography` (werkzeug comes with flask). The core imports both at load time.
- `git`, if you use a clone (step 3). Without git, use a zip of the commit.

Tested by us (internal) on:
- Windows 11 (10.0.26200), Python 3.12.10, flask 3.1.3, werkzeug 3.1.8, cryptography 43.0.3, git 2.55.0.windows.5: 11.2-12.3 s over three runs.
- Ubuntu under WSL2 (kernel 6.18), Python 3.14.4, flask 3.1.3, werkzeug 3.1.8, cryptography 46.0.5, git 2.53.0: 4.7 s.

Not tested: macOS, Python 3.10 or 3.11, other versions of flask or cryptography, a container, a real VM.

## 3. Get the pinned commit

Either clone (any recent clone of `main` contains it):

```bash
git clone https://github.com/LAWLESS1987/covenant
```

or fetch only that commit:

```bash
git init covenant && git -C covenant fetch --depth 1 https://github.com/LAWLESS1987/covenant 9d85f6c902bcfab4616be0d3b08d0715584f7a07
```

or download `https://github.com/LAWLESS1987/covenant/archive/9d85f6c902bcfab4616be0d3b08d0715584f7a07.zip` and unpack
it. The repository stores LF line endings. If your unzip tool converts them to CRLF, the blob check refuses the files
(exit 2); a clone avoids that.

## 4. Run it

```bash
python run_packet.py --covenant path/to/covenant
```

Options: `--out DIR` (where the record goes; default `./signed_run_packet_out_<UTC time>`), `--keep` (keep the
temporary folder to look inside it).

## 5. What it runs

Three scripts: APPROVED (writes `ran_approved.txt`), CHANGED (writes `ran_changed.txt`) and SUBSTITUTE (writes
`ran_substitute.txt`). The signed request is always the JSON body `{"run_sha256": sha256(APPROVED)}` sent to
`POST /m/agent`.

| case | setup | expected |
|---|---|---|
| 1 signed, no arguments | probe.py is APPROVED; signed; answer `HANDS RUN probe.py` | APPROVED runs, in exactly 1 child |
| 2 changed bytes | probe.py is CHANGED; signed hash is of APPROVED | nothing runs, no child |
| 3 added arguments | APPROVED; signed; answer `HANDS RUN probe.py --extra 1` | nothing runs, no child |
| 4 unsigned | APPROVED; same body, no signature headers | nothing runs, no child |
| 5a swap at launch | as 1; the moment the child is launched (after the hash check and the screen), probe.py is overwritten with SUBSTITUTE | SUBSTITUTE never runs; APPROVED runs (or nothing runs) |
| 5b continuous swap | as 1; from the gate (after the single read) until the act returns, a thread keeps replacing probe.py with SUBSTITUTE | same as 5a |

**"Ran" and "refused" mean what happened, not what the code said.** A case is judged only by which marker files
exist in its workshop afterwards and how many child processes the hands started. Two routes that can disagree. The
door's reply text and its ledger row are printed in the record for you to read, but they decide nothing. In case 5 the
packet also checks that the swap really happened (probe.py is SUBSTITUTE afterwards); a swap that never happened
would make the case test nothing, and it then fails.

## 6. The seven variants: proving the checks can fail

The same cases run against seven copies of the code. Each break is one exact text replacement, listed in
`run_packet.py` (`MUTATIONS`).

| variant | what is broken | must fail |
|---|---|---|
| pinned | nothing | none |
| always_refuse | every signed run is refused | case 1 only |
| accept_everything | all four guards removed at once | cases 2, 3, 4, 5a, 5b |
| no_signature_check | the door treats every request as signed | case 4 only |
| no_hash_check | the hash comparison never refuses | case 2 only |
| no_args_check | the argument refusal never fires | case 3 only |
| child_reopens | the child opens probe.py by name (the runner before A430) | 5a and 5b only |

A variant is "as pre-registered" when it fails **exactly** its listed cases. If the cases could not tell working code
from broken code, these lines would show it.

## 7. Reading the result

The last line is `RESULT: ... exit N`.
- **exit 0**: all seven variants as pre-registered, and no network event, unexpected module or outside write was seen.
- **exit 1**: something differs from `expected.json`. The table shows which variant and case. This is the result we
  most want to hear about.
- **exit 2**: it could not run: wrong Python, a missing package, source files that don't match the commit, a break
  whose text was not found, or a worker that crashed. Nothing was judged. (v1 writes no record folder on exit 2;
  copy the console output.)

The output folder holds `summary.txt` (the printed table), `results.json` (every case's observations and verdict),
`workers_raw.json` (each worker's command, exit code, stdout and stderr, timing) and `environment.json` (Python,
platform, package versions, the command, and the sha256 of `run_packet.py` and `expected.json` as you ran them).

Notes from our runs:
- On Windows, under `child_reopens`, case 5b failed because the child's own open hit `PermissionError` while the file
  was being replaced. On Linux the substitute ran. Both count as a failure under the rule written before the first
  run: one child started, and the approved marker is absent.
- The sha256 of `run_packet.py` in `environment.json` is of the file's bytes as you hold it. A copy with converted
  line endings gives a different hash and still runs.

## 8. Not tested here

- A deployed node, the HTTP layer, and the rest of the `/m/agent` route. The packet runs the HANDS branch out of
  the core's syntax tree in a test request context, as covenant's own `test_a430_run_sha256.py` does.
- The model, and the shared quorum (stubbed to "clean").
- The screen, and what a script can do once it runs: containment, network egress, child processes.
- Key theft, and revocation (there is none).
- A key that signs validly but is not registered (refused in the source; no case here).
- The owner's in-process paths (practice loop, console), which run without a signature by design.
- Symlinks, oversize files, malformed hashes (covenant's own tests cover several of these).
- Timing races other than the two swap points above.

## 9. Sending it back

`REVIEWER_RETURN.md` is a template. Fill in what you're comfortable sharing. Anything you had to change, and any case
that came out differently, is the most useful part. With your OK, we would publish your result beside ours, both kept
as they are.
