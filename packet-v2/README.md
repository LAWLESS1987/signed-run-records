# Signed-RUN reproduction packet, v2.4

At one pinned commit of covenant's source, not a deployed system, and only for the fifteen cases below, this packet
checks one narrow rule on your own machine with one command:

> At covenant commit `ead187b2513fba7bce1404cf3678ae128f38b1b8`: the operator's signed request
> names the script by the SHA-256 of the script file's bytes, and a script whose bytes don't match is refused; a
> signed run that carries arguments is refused; an unsigned run is refused. The bytes are read once and never
> reopened.

`CLAIM.md` reads that claim against the source line by line. It says exactly what the packet measures and what stays
a reading of the source. v2.3, pinned to `9d85f6c`, found that an **ally** key with the default scope could also
authorize a run, wider than "the operator's signed request" (case C1). At this pin that is closed (covenant A447):
only one of the operator's own registered keys may authorize a run, so C1 is pre-registered as refused. The text a
refused RUN hands the model now states that rule too (A446, found by Jang-woo).

Passing these cases would not show that covenant is secure, contained or deployed. It would show only that this rule
held on your machine for these cases.

Written by Claude (an AI) for the Mutual Benefit Collective, issue #21, at Lawrence's direction. ChatGPT reviewed v1
and did not pass it; v2 answers that review, and DeepSeek reviewed v2.1. Both reviews and `CHANGES.md` (every version
and why it changed) are published beside this README. v2.4 adds capitaharlock's case (a planted `json.py` must not
load) and its control, and answers nootxlm's three points on v2.3 (`CHANGES.md`). Our own runs are **internal
preparation**, summarised in
`RUNS_SUMMARY.md`. The raw records are kept in the collective's repository, which is private. A run on your machine
is the outside reproduction, and it is yours: report what you saw, including anything that differs from ours.

**Outside runs of v2.3** (pinned to `9d85f6c`, so C1 ran there, as pre-registered): nootxlm, on native Linux with no
network, 11 of 11, with a claim audit and the full run record at
https://github.com/1OF1Research/covenant-signed-run-check-2026-11-17; and Jang-woo, run for him by Claude in
Anthropic's cloud workspace on a cloud VM, 11 of 11 twice (https://discuss.huggingface.co/t/we-gave-ai-a-trust-we-never-gave-people-the-third-axis-after-capability-and-permission/183807/44). Both are theirs, as they reported them.

Jang-woo's return files, with his own `SHA256SUMS.txt`, are at
https://gist.github.com/Jang-woo-AnnaSoft/b9986a5ce94ac434725f6e2154ac2a59 (revision `b48a49c7`). We checked that
his `SHA256SUMS.txt` has the hash he posted and that the 13 files it lists match it. Of the packet files, we compared
only the `run_packet.py` and `expected.json` hashes in his return, which match our published v2.3. We did not run his
extra cases (`extra_cases.py`).

This README was revised on 2026-11-19 to add three of our runs to section 4 and the link above. `run_packet.py`,
`expected.json`, `CLAIM.md` and `REVIEWER_RETURN.md` did not change; `RUNS_SUMMARY.md` gained the same three runs,
and `CHANGES.md` says what changed and why.

To run it, you need `run_packet.py` and `expected.json` in the same folder. The other files are for reading.

## 1. What there is to read

Please read before you run. A VM or container is fine.

- **The packet:** three files you run or that decide the result. `run_packet.py` (the only code), `expected.json`
  (every observation, written and committed before our first run of v2) and this README. Plus two text files:
  `CLAIM.md` and `REVIEWER_RETURN.md`.
- **The claim's code path in covenant:** short. The line ranges are in the table below.
- **All the covenant code that executes:** not small. The packet imports nine covenant files totalling 21,064 lines
  (14,077 of them in `covenant_unified_v8.py`, the node's core), and importing them runs their module-level code. Our
  invitation said "every file is small, so read it all first". That is true of the packet. It is not true of the
  covenant code it loads, and we said it wrongly. The correction is recorded as retraction SRP-SMALL-1 in the
  collective's `docs/RETRACTED.json`.

| file | lines (at the pin) | what |
|---|---|---|
| `covenant_unified_v8.py` | 9518-9640 | the `/m/agent` door's HANDS branch; who may run is decided at line 9530, `run_sha256` is read at line 9537 |
| `covenant_unified_v8.py` | 559-573 | `_request_signed_by_registered`: the address never grants a run, and only an operator signer passes (A447) |
| `covenant_unified_v8.py` | 1951-2014 | key generation, the signed message, signing and verifying |
| `covenant_mycelium.py` | 114-167 | `admit`: operator signers, then allies on their doors |
| `covenant_daily_plan.py` | 357-385 | `verify_signed`: registered key, 300 s window, single-use nonce |
| `covenant_daily_plan.py` | 95-123 | `nonce_check_and_record`: the durable nonce store (A444), via `pairstore_excl.py` |
| `covenant_tetsu_hands.py` | 246-261 | RUNNER: the child reads its code from standard input |
| `covenant_tetsu_hands.py` | 488-546 | `_binding_refusal` and `run()`: hash, screen and launch the same bytes (`-I` at line 536) |
| `covenant_tetsu_hands.py` | 689-703, 764-799 | `parse` (where arguments come from), `_capture` and `_captured` (the single read) |
| `covenant_tetsu_hands.py` | 914-1065 | `act()`: the order of the refusals; the refusal text is `RUN_REFUSED_DATA` (line 909) |

With only the packet's nine files present, `covenant_semantic_judge` prints a warning that it has no model file.
That is expected; the judge is not used.

## 2. What it does on your machine

- It reads the nine files at the pinned commit and checks each against its git blob hash. From a clone it uses
  `git cat-file` on the object store, not the working tree, with `GIT_NO_LAZY_FETCH=1`; from a folder it reads the
  files. On any mismatch it stops with exit 2 before running anything.
- It makes one temporary folder (Python `tempfile`, prefix `signed_run_packet_`), deletes it at the end unless you
  pass `--keep`, and writes the record into the output folder.
- It starts one worker Python process per variant (twelve). Each worker starts child Python processes that run four
  tiny scripts, printed in full in `run_packet.py` (`SCRIPTS`, and `PLANTED_JSON` for case 10). Each script writes one
  marker file in its temporary workshop and prints one line. That is all a script under test does.
- **Importing the core patches the worker process** (nootxlm's first point on v2.3). `covenant_unified_v8.py` calls
  `_imports_fingerprint()` at module level (line 501), which imports `covenant_watchdog`, whose line 72 calls
  `covenant_quiet.install()` (`covenant_quiet.py` lines 164-173). That replaces `subprocess.Popen.__init__` for the whole
  process, on every platform. Off Windows it changes nothing. On Windows it adds a flag that keeps a console window
  from opening and, when the program is `pythonw`, swaps in its console twin (`_quiet_init`, lines 118-127). Every launch
  the packet observes goes through that patched `Popen`. The patch ends by calling the original `Popen.__init__`,
  which raises the audit event the packet reads, so a launch is still seen, with the arguments as the patch passed
  them on. It is covenant code on the path, not plain Python.
- It generates three RSA keys in memory per worker: the operator's, a stranger's and an ally's. Only their public
  halves are written, into temporary files. No key of ours is involved.

**What is observed, and what is not.** Each worker installs a Python audit hook before importing covenant. It records
socket events, launches of child processes, the worker's own opens of the script file, and files the worker opens for
writing outside the temporary folder. The run reports any of these it should not see. On our runs it saw no socket
event and no outside write. This covers the worker process only. It does not cover the main process (which runs `git`
and starts the workers), `git` itself, or the children running the scripts. It is an observation, not a sandbox or a
firewall.

**Network.** The run needs none once you have the files. The worker inherits your environment (all but `COVENANT_*`
variables), so nothing stops the code from using the network; the hook would only report it. For a fully offline
run: get the files first (section 3), disconnect, run with the plain-folder route, and say so in your return.

## 3. Setup

You need Python 3.10 or newer, `flask` and `cryptography` installed into **the same Python you run the packet with**,
and `git` if you use a clone.

Linux or macOS:

```bash
python3 -m venv venv
```

If that fails on Debian or Ubuntu, install the distribution's venv package (`python3-venv`) and try again.

```bash
venv/bin/python -m pip install flask cryptography
```

```bash
git clone https://github.com/LAWLESS1987/covenant
```

Windows (PowerShell; if `py` is not installed, use `python`):

```powershell
py -3 -m venv venv
```

```powershell
venv\Scripts\python -m pip install flask cryptography
```

```powershell
git clone https://github.com/LAWLESS1987/covenant
```

Any clone of `main` made after the pin contains the pinned commit; the packet reads that commit, whatever is checked
out. Without git: download `https://github.com/LAWLESS1987/covenant/archive/ead187b2513fba7bce1404cf3678ae128f38b1b8.zip`, unpack
it, and pass the folder that contains `covenant_unified_v8.py` (normally `covenant-ead187b2513fba7bce1404cf3678ae128f38b1b8`).
The repository stores LF line endings. If your unzip tool converts them to CRLF, the blob check refuses the files
(exit 2).

## 4. Run it

From the folder holding `run_packet.py`. Linux or macOS:

```bash
venv/bin/python run_packet.py --covenant path/to/covenant
```

Windows:

```powershell
venv\Scripts\python run_packet.py --covenant path\to\covenant
```

Options: `--out DIR` (where the record goes; default `./signed_run_packet_out_<UTC time>`), and `--keep` (keep the
temporary folder so you can look inside it).

Tested by us (internal), v2.4 against `ead187b`, each with exit 0 and 12 of 12 variants as pre-registered (runs 1
and 3, not listed here, each found a defect in the harness, not in covenant; `CHANGES.md` and `RUNS_SUMMARY.md` keep
them):

| OS | Python | flask / werkzeug / cryptography | git | how | runs | time |
|---|---|---|---|---|---|---|
| Windows 11 (10.0.26200) | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | 2.55.0.windows.5 | covenant read from a clone's object store at the pin | 1 | 25.8 s |
| Ubuntu on WSL2 (kernel 6.18) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | 2.53.0 | the nine files as a plain folder (`git archive` of the pin) | 1 | 9.2 s |
| Windows 11 (10.0.26200) | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | 2.55.0.windows.5 | **this gist cloned, a full `git clone` of covenant**, read from its object store at the pin (packages already in that Python) | 1 | 25.4 s |
| Ubuntu on WSL2 (kernel 6.18) | 3.10.21, new venv | 3.1.3 / 3.1.9 / 50.0.2 | 2.53.0 | the nine files as a plain folder; network cut, environment emptied (below) | 1 | 10.2 s |
| Ubuntu on WSL2 (kernel 6.18) | 3.11.16, new venv | 3.1.3 / 3.1.9 / 50.0.2 | 2.53.0 | the same | 1 | 9.2 s |

The 3.10.21 and 3.11.16 rows (2026-11-19, after capitaharlock's note that case 10 was untested there): uv's Python
builds, a new venv for each with only flask and cryptography installed by uv (werkzeug came with flask), and this
packet's `run_packet.py` and `expected.json` with their published bytes (both git blob hashes, taken with
`--no-filters`, matched ours, given under "Checking you have our files" below). The run had no network (a new network namespace, `unshare -rn`) and an emptied
environment (`env -i`, then only `PATH`, `HOME`, `LANG` and two git settings set). All nine covenant files matched
their pinned hashes. In both, case 10 came out as pre-registered both ways: under the pin the planted `json.py` did
not load, and under `no_isolation` it did.

v2.1, v2.2 and v2.3, against `9d85f6c`, each with exit 0 and 11 of 11 variants as pre-registered:

| OS | Python | flask / werkzeug / cryptography | git | how | runs | time |
|---|---|---|---|---|---|---|
| Windows 11 (10.0.26200) | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | 2.55.0.windows.5 | packet from our record; covenant fetched at the pin, or as a plain folder | 5 | 21.8-24.3 s |
| Ubuntu on WSL2 (kernel 6.18) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | 2.53.0 | the same | 3 | 8.4-8.7 s |
| Windows 11 | 3.12.10, new venv | 3.1.3 / 3.1.9 / 50.0.2 | 2.55.0.windows.5 | **this gist cloned, a full `git clone` of covenant, packages installed by pip as in section 3** | 1 | 43.1 s |
| Ubuntu on WSL2 | 3.14.4, system Python | 3.1.3 / 3.1.8 / 46.0.5 | 2.53.0 | this gist cloned, a full `git clone` of covenant | 1 | 17.9 s |

On that Ubuntu, `python3 -m venv venv` failed because the `python3-venv` package was not installed. The run used the
system Python, which already had flask and cryptography. Without them, the packet stops with exit 2 and names the
command to install them.

Not tested by us: macOS, native Linux outside WSL, Python versions not in these tables, a container, a real VM. (nootxlm ran v2.3 on
native Linux in a VM, and Jang-woo had it run on a cloud VM; see the top of this README.)

**Checking you have our files.** Git for Windows normally converts line endings to CRLF when it clones. The sha256
of `run_packet.py` that the run prints then differs from ours. To compare in a way line endings cannot change, run
`git hash-object run_packet.py expected.json` in your copy. Ours (v2.4) are `c008b5203d1ca852e152b7dd3a9b76bfc4f3862b`
and `4fdb71c207ead8e785fd2723b5ce8a7b00357608`. (v2.3's were `03214394...` and `01b97e9e...`.) Git blob hashes do not depend on line endings; for v2.2 we measured them the same in a CRLF checkout and an LF one. The covenant
files are not affected, because the packet reads them from git's object store.

## 5. The cases

Three scripts: APPROVED, CHANGED and SUBSTITUTE, each writing `ran_<name>.txt`, and for case 10 IMPORTS_JSON (imports
`json`, then writes the approved marker) with PLANTED_JSON beside it as `json.py` (writes `ran_planted.txt` if it is
imported). Unless a case says otherwise, the
request is `POST /m/agent` from 127.0.0.1 with the JSON body `{"run_sha256": sha256(APPROVED)}`, signed by the
registered operator key, and the model's answer line is `HANDS RUN probe.py`.

| case | what changes | pinned code |
|---|---|---|
| 1 signed, no arguments | nothing | APPROVED runs, no child arguments |
| 2 changed bytes | probe.py is CHANGED | nothing launched |
| 2b one byte added | probe.py is APPROVED plus one newline | nothing launched |
| 3 added arguments | answer `HANDS RUN probe.py --extra 1` | nothing launched |
| 3b one argument | answer `HANDS RUN probe.py x` | nothing launched |
| 4 unsigned, loopback | no signature headers; caller 127.0.0.1 | nothing launched |
| 4b unsigned, tailnet | no signature headers; caller 100.127.255.254 | nothing launched |
| 5a swap at launch | at the launch call (after the hash check and the screen), probe.py is replaced by SUBSTITUTE, confirmed, then the launch goes ahead | APPROVED runs; SUBSTITUTE does not |
| 5b continuous swap | from the gate (after the single read) until the act returns, a thread keeps replacing probe.py with SUBSTITUTE; the gate waits for the first confirmed replacement | APPROVED runs; SUBSTITUTE does not |
| 6 body changed after signing | headers signed for `{"run_sha256": sha256(CHANGED)}`, body sent says sha256(APPROVED) | nothing launched |
| 7 bad signature, registered key | a real signature by the registered key, over a different body | nothing launched |
| 8 unregistered key | validly signed by a key registered nowhere | nothing launched |
| 9 signed, no hash | signed body `{"text": "please run it"}` | nothing launched |
| 10 planted json.py (v2.4) | probe.py is IMPORTS_JSON, signed for its own hash; `json.py` planted beside it | IMPORTS_JSON runs; the planted file does not load |
| C1 ally key (characterization) | signed by a key registered as an ally with the default scope | nothing launched (at v2.3's pin it ran) |

Every case also counts the parent's opens of probe.py while the door handles the request. On the pinned code it is 1
in every case.

**Only what happened counts.** Each case gets one outcome:
- RAN_APPROVED, RAN_CHANGED or RAN_SUBSTITUTE: exactly that marker exists, with the right content, after at least one
  launch attempt.
- NOTHING: no marker and no launch attempt.
- LAUNCH_NO_MARKER: a launch was attempted and no marker exists.
- INCONCLUSIVE: the harness raised an error, there was more than one marker or a marker with the wrong content, a
  marker appeared with no launch attempt, or a swap case launched without a confirmed swap before the launch.

A LAUNCH_NO_MARKER where the table expects a script to run (case 1, say) is reported as a difference (exit 1), not as
inconclusive, because a broken guard can look like that too. Before reading it as a guard failure, look at that
worker's `stderr` in `workers_raw.json`: a child that could not start or could not write its marker is an
environment problem, and we would want to hear about it either way.

The door's reply text and its ledger row are in `results.json` for you to read. They decide nothing. At this pin a
refused RUN's text states who may run (A446); at v2.3's pin it still said loopback was enough, which was never the rule
the door applied.

## 6. The twelve variants: proving the checks can fail

The same fifteen cases run against twelve copies of the code. Each break is one exact text replacement, listed in
`run_packet.py` (`MUTATIONS`), and `expected.json` says, for each copy, what every case must show.

| variant | what is broken | what changes from the pinned column |
|---|---|---|
| pinned | nothing | (the pinned column) |
| always_refuse | every bound run is refused | 1, 5a, 5b and 10 launch nothing |
| accept_everything | signature, hash, argument and read-once guards all removed | 2 to 9 and C1 all run something; 5a/5b run SUBSTITUTE (5b on Windows may instead launch with no marker) |
| no_signature_check | the door treats every request as signed | 4, 4b, 6, 7, 8 and C1 run |
| no_hash_check | the hash never refuses | 2 runs CHANGED; 2b and 9 run |
| no_args_check | the argument refusal never fires | 3 and 3b run, and the child receives the arguments |
| child_reopens | the child opens probe.py by name | 5a runs SUBSTITUTE; 5b runs SUBSTITUTE or launches with no marker |
| extra_parent_read | run() opens probe.py once more and discards it | nothing runs differently; 1, 5a, 5b and 10 count 2 reads |
| no_body_digest | the signature stops covering the body | 6 runs |
| no_signature_verify | signatures are never checked | 6 and 7 run |
| no_registry_check | a key need not be registered | 8 and C1 run (the ally key passes as an unregistered operator key) |
| no_isolation (v2.4) | the child is launched without `-I` | 10: the planted `json.py` loads |

## 7. Reading the result

The last line is `RESULT: ... exit N`.
- **exit 0**: every variant as pre-registered. Nothing inconclusive, no socket event, no unexpected module, no
  outside write.
- **exit 1**: an observation differs from `expected.json`. The table marks it `DIFF` and says how. This is the result
  we most want to hear about.
- **exit 2**: it could not run (Python, a missing package, source files that don't match, git missing, a break whose
  text was not found, a worker that failed or ran past 600 s). Nothing was judged.
- **exit 3**: a fixture did not do its part (INCONCLUSIVE). The case says why.

The output folder holds `summary.txt` (the table), `results.json` (every observation, expectation and verdict),
`workers_raw.json` (each worker's command, exit code, stdout, stderr and time) and `environment.json` (Python,
platform, package versions, the command, and the sha256 of `run_packet.py` and `expected.json` as you ran them). It is
written for every run that gets past the command line, whatever the exit code. These files contain your local paths; see `REVIEWER_RETURN.md` on redacting them.

## 8. Not tested here

- A deployed node, the HTTP layer, and the rest of the `/m/agent` route. The packet runs the HANDS branch out of the
  core's syntax tree in a test request context, as covenant's own `test_a430_run_sha256.py` does.
- The model, and the shared quorum (stubbed to "clean").
- The screen, and what a script can do once it runs: containment, network egress, its own child processes.
- Key theft, and revocation (there is none).
- Ally keys at doors other than this RUN. C1 covers only the ally's signed RUN through `/m/agent`.
- Replay of a signed request after a restart or from a second process. The nonce store is durable at this pin (A444),
  and covenant's own `test_a444_nonce_store.py` tests that; the packet points the store into its temporary folder and
  runs each case once.
- What `-I` does not cover: the approved script itself can still put its workshop on `sys.path` and import a
  neighbour, whose bytes are not hashed. Case 10 shows only that the launch does not do it for the script.
- Python versions we have not run (section 4 lists the ones we have), unless your run covers them.
- The owner's in-process paths (practice loop, console), which run without a signature by design.
- What the child does with its standard input beyond these cases. The child is not audited, so "never reopened" is
  shown only by the swap cases.
- Symlinks, oversize files and malformed hashes. Covenant's own tests cover several of these.
- Other timing schedules than the two swaps.

## 9. Sending it back

`REVIEWER_RETURN.md` is a template. Fill in what you're comfortable sharing. Anything you had to change, and any case
that came out differently, is the most useful part. With your OK, we would publish your result beside ours, both kept
as they are.
