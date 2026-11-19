# Internal preparation runs of v2, v2.1 and v2.2, 2026-11-17 (NOT an outside reproduction)

Run by Claude (an AI) on Lawrence's PC. Each run used the packet files exactly as committed, copied out with
`git show <commit>:reviews/signed-run-packet-2026-11-17/packet-v2/<file>` into a new scratch folder. The covenant
source came from a fresh fetch of the pinned commit:
`git init -q cov`, then `git -C cov fetch -q --depth 1 https://github.com/LAWLESS1987/covenant 9d85f6c902bcfab4616be0d3b08d0715584f7a07`.
Raw output, kept byte for byte (`../.gitattributes`: `-text`).

| run | packet commit | run_packet.py sha256 | where | source | result | exit | time |
|---|---|---|---|---|---|---|---|
| v2.0_run1_harness_defect | 30d6425 (v2) | 90c2e156... | Windows 11, Python 3.12.10 | clone | INCONCLUSIVE, 1 of 11 as pre-registered | 3 | 22.0 s |
| v2.1_run1 | 5312539 (v2.1) | ec794ce6... | Windows 11, Python 3.12.10 | clone | 11 of 11 as pre-registered | 0 | 22.0 s |
| v2.1_run2 | 5312539 | ec794ce6... | Windows 11, Python 3.12.10 | clone | 11 of 11 | 0 | 23.2 s |
| v2.1_run3 | 5312539 | ec794ce6... | Windows 11, Python 3.12.10 | plain folder (`git archive`, the zip route) | 11 of 11 | 0 | 21.8 s |
| v2.1_run4_wsl | 5312539 | ec794ce6... | Ubuntu on WSL2, Python 3.14.4 | clone, in the Linux home folder | 11 of 11 | 0 | 8.7 s |
| v2.2_run1 | 5b4fcf8 (v2.2) | e348f5ec... | Windows 11, Python 3.12.10 | clone | 11 of 11 | 0 | 22.6 s |
| v2.2_run2_wsl | 5b4fcf8 | e348f5ec... | Ubuntu on WSL2, Python 3.14.4 | clone, in the Linux home folder | 11 of 11 | 0 | 8.6 s |

`expected.json` sha256 `6cd5960bdc87c4ca0fdbdf42bad326da5b0befd61e16c39174533067d59c4538` in all seven (unchanged from
v2 to v2.2). Full hashes are in each run's `environment.json`.

Command in each: `python packet/run_packet.py --covenant cov --out out` (`--covenant zipdir` in v2.1_run3; `python3`
in WSL).

## v2.0 run 1: the harness, not covenant, was wrong

Exit 3. Every swap case was INCONCLUSIVE ("a launch with no swap confirmed before it"), and every launch's child
arguments read as `['<unrecognized launch>', 'None']`. Two causes, both Windows-specific and both in the harness
(`../../CHANGES.md`): the `subprocess.Popen` audit event carries one command-line string there, not a list; and
`time.monotonic()` has a resolution of 0.015625 s, so the swap and the launch read as simultaneous. In the same run,
every marker file, read count and swap count was what `expected.json` predicted (`results.json`). Kept as it came out.

## v2.1: what the runs showed

- Pinned code, all four runs: 1, 5a, 5b and C1 RAN_APPROVED with no child arguments. Every other case NOTHING (no
  launch). One parent read of probe.py in every case.
- The read count and the child arguments, driven both ways: `extra_parent_read` shows 2 reads where the pinned code
  shows 1; `no_args_check` and `accept_everything` show the child receiving `['--extra', '1']` and `['x']`, where the
  pinned code launches nothing.
- Case 5b under `child_reopens` and `accept_everything` was RAN_SUBSTITUTE on Linux (v2.1_run4_wsl) and in 5 of the 6
  Windows instances. The sixth, `accept_everything` in v2.1_run2, was LAUNCH_NO_MARKER. The pre-registration allows
  either, because v1's Windows runs had shown the child's open failing with PermissionError mid-replace. On the pinned
  code 5b was RAN_APPROVED every time.
- No worker saw a socket event, an outside write or an unexpected module.

## The exit-2 paths, driven (v2.1_run3/exit2_paths)

- `tampered`: one byte appended to `covenant_tetsu_hands.py`. SOURCE CHECK FAILED, exit 2, nothing ran. The record
  folder was written (v1 left it empty).
- `empty`: an empty folder passed as `--covenant`. SOURCE CHECK FAILED ("cannot read covenant_daily_plan.py"), exit
  2, record written. In v1 this was an uncaught exception.

## v2.2 (DeepSeek's minor points)

Two clean runs, Windows and WSL, both 11 of 11 as pre-registered, exit 0. `v2.2_run1/exit2_no_expected_json`: `run_packet.py` run from a folder without `expected.json` prints `COULD NOT RUN: expected.json next to run_packet.py is missing or unreadable` and exits 2. That is the new path, driven once. The unwritable-output-folder path was not driven.
