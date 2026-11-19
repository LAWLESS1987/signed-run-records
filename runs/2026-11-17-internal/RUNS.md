# Internal preparation runs, 2026-11-17 (NOT an outside reproduction)

Run by Claude (an AI) on Lawrence's PC. Every run used the packet files exactly as committed in `024cb2f` (the
pre-registration commit), copied out with `git show 024cb2f:<path>` into a new folder. The covenant source came from
a fresh fetch of the pinned commit, never from a working tree anyone edits.

Packet file hashes as run: `run_packet.py` sha256 `07f063601bc501ae319a77994f8d369108a7ba6e137aa2d60c73da8cdb6ce935`,
`expected.json` sha256 `b7614f3cf4414e0626b2dfe652fb4fbf9137cb0e6656f55f9dbc5e981eef7f74` (each run's
`environment.json` records them again).

Files here are raw output, kept byte for byte (`.gitattributes`: `-text`).

## Setup, the same for runs 1-3 (Windows), in a new scratch folder each time

```
git init -q cov
git -C cov fetch -q --depth 1 https://github.com/LAWLESS1987/covenant 9d85f6c902bcfab4616be0d3b08d0715584f7a07
git -C <collective clone> show 024cb2f:reviews/signed-run-packet-2026-11-17/packet/run_packet.py > packet/run_packet.py
git -C <collective clone> show 024cb2f:reviews/signed-run-packet-2026-11-17/packet/expected.json > packet/expected.json
```

## The runs

| run | where | source mode | command | result | exit | time |
|---|---|---|---|---|---|---|
| 1 | Windows 11, Python 3.12.10 | clone (git object store) | `python packet/run_packet.py --covenant cov --out out --keep` | 7 of 7 as pre-registered | 0 | 12.3 s |
| 2 | Windows 11, Python 3.12.10 | clone | `python packet/run_packet.py --covenant cov --out out` | 7 of 7 | 0 | 11.4 s |
| 3 | Windows 11, Python 3.12.10 | plain folder (`git archive` of the clone, the zip route) | `python packet/run_packet.py --covenant zipdir --out out` | 7 of 7 | 0 | 11.2 s |
| 4 | Ubuntu on WSL2, Python 3.14.4 | clone, in the Linux home folder | `python3 packet/run_packet.py --covenant cov --out out` | 7 of 7 | 0 | 4.7 s |

Each run folder holds `console.txt` (everything printed, with `EXIT n` appended by the shell), and the packet's own
`summary.txt`, `results.json`, `workers_raw.json` and `environment.json`.

In all four runs, every worker's audit hook recorded no socket event, no file opened for writing outside the
temporary folder, and no module loaded from the source folder beyond the eight pinned files (`results.json`:
`network_events`, `writes_outside_root`, `unexpected_source_files`).

## The source check, driven both ways (run3/source_guard)

From copies of run 3's plain folder:
- one byte (`\n`) appended to `covenant_tetsu_hands.py`: `SOURCE CHECK FAILED`, exit 2, nothing ran;
- `covenant_mycelium.py` converted to CRLF: `SOURCE CHECK FAILED`, exit 2, nothing ran.

The untouched folder (run 3) passes it, so the check reads the bytes it claims to read.

## Covenant's own tests at the pin (covenant_tests_at_pin)

From a `git archive` of `9d85f6c` into a scratch folder, `python -B <test>`: `test_a430_run_sha256.py` 18/18,
`test_a430_run_signing.py` 13/13, `test_a436_run_args_bind.py` 5/5, `test_th1_tetsu_hands.py` 31/31, each exit 0.
These are covenant's own checks, not the packet's.

## What the runs showed beyond pass and fail

- **Case 5b under `child_reopens` fails differently by OS.** Windows (runs 1-3): the child's open of probe.py hit
  `PermissionError` while the file was being replaced, so the child exited 1 and wrote no marker. Linux (run 4): the
  SUBSTITUTE script ran (12 swap writes). Both are failures under the rule committed before the first run: one child
  started and the approved marker is absent.
- **Under `always_refuse`, case 5a's swap never happened**, because the launch it is tied to never came
  (`disk_after=approved`). The pre-registered rule accepts "nothing ran, no child started" for case 5, as the claim
  does ("only the signed bytes run, or nothing does").
- **On the pinned code, cases 5a and 5b showed `approved_ran` in every run,** as pre-registered
  (`pinned_expected_detail`).
- **Exit 2 leaves the `--out` folder empty** (seen in the source-guard runs). v1 writes its record only after the
  variants ran. The README says so and asks for the console output in that case.
