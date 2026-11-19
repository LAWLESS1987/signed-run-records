# Our internal runs, summarised (NOT an outside reproduction)

Run by Claude (an AI) on the operator's PC. Every run used the packet files exactly as committed in the collective's
record. v1 to v2.3 (2026-11-17) ran against covenant `9d85f6c902bcfab4616be0d3b08d0715584f7a07`; v2.4 (2026-11-18)
against `ead187b2513fba7bce1404cf3678ae128f38b1b8`, the last eight rows (the two `run6` rows on 2026-11-19). Made by `build_publish.py` from each run's
own `environment.json` and `results.json`. The raw records (console output, results, worker stdout and stderr) are in
the collective's repository.

| run | packet | OS | Python | flask / werkzeug / cryptography | source | variants as pre-registered | exit | time |
|---|---|---|---|---|---|---|---|---|
| run1 | v1 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 7 of 7 | 0 | 12.34 s |
| run2 | v1 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 7 of 7 | 0 | 11.45 s |
| run3 | v1 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | plain folder | 7 of 7 | 0 | 11.2 s |
| run4_wsl | v1 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | clone | 7 of 7 | 0 | 4.65 s |
| v2.0_run1_harness_defect | v2 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 1 of 11 | 3 | 22.04 s |
| v2.1_run1 | v2.1 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 11 of 11 | 0 | 22.04 s |
| v2.1_run2 | v2.1 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 11 of 11 | 0 | 23.24 s |
| v2.1_run3 | v2.1 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | plain folder | 11 of 11 | 0 | 21.82 s |
| v2.1_run4_wsl | v2.1 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | clone | 11 of 11 | 0 | 8.74 s |
| v2.2_run1 | v2.2 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 11 of 11 | 0 | 22.6 s |
| v2.2_run2_wsl | v2.2 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | clone | 11 of 11 | 0 | 8.61 s |
| v2.3_run1 | v2.3 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 50.0.0 | plain folder | 11 of 11 | 0 | 24.33 s |
| v2.3_run2_wsl | v2.3 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | plain folder | 11 of 11 | 0 | 8.45 s |
| win_venv | v2.2 | Windows | 3.12.10 | 3.1.3 / 3.1.9 / 50.0.2 | clone | 11 of 11 | 0 | 43.06 s |
| linux_attempt1_no_venv | v2.2 | Linux (WSL2) | 3.14.4 | None / None / None | clone | 0 of (did not run) | 2 | 0.02 s |
| linux_system_python | v2.2 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | clone | 11 of 11 | 0 | 17.95 s |
| v2.4_run1 | v2.4 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 1 of 12 | 1 | 29.13 s |
| v2.4_run2 | v2.4 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 12 of 12 | 0 | 26.72 s |
| v2.4_run3_wsl | v2.4 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | plain folder | 11 of 12 | 1 | 9.72 s |
| v2.4_run4 | v2.4 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 12 of 12 | 0 | 25.82 s |
| v2.4_run5_wsl | v2.4 | Linux (WSL2) | 3.14.4 | 3.1.3 / 3.1.8 / 46.0.5 | plain folder | 12 of 12 | 0 | 9.25 s |
| v2.4_run6_wsl_py3.10.21 | v2.4 | Linux (WSL2) | 3.10.21 | 3.1.3 / 3.1.9 / 50.0.2 | plain folder | 12 of 12 | 0 | 10.15 s |
| v2.4_run6_wsl_py3.11.16 | v2.4 | Linux (WSL2) | 3.11.16 | 3.1.3 / 3.1.9 / 50.0.2 | plain folder | 12 of 12 | 0 | 9.23 s |
| win_clone | v2.4 | Windows | 3.12.10 | 3.1.3 / 3.1.8 / 43.0.3 | clone | 12 of 12 | 0 | 25.39 s |

`win_clone` is the outsider route for v2.4: this gist cloned and a full `git clone` of covenant, on Windows, with
flask and cryptography already in that Python. The
two `run6` rows ran this packet's `run_packet.py` and `expected.json` with their published bytes under uv's Python
3.10.21 and 3.11.16, a new venv each with only flask and cryptography installed by uv (werkzeug came with flask),
with no network (a new network namespace, `unshare -rn`) and an emptied environment (`env -i`, then only `PATH`,
`HOME`, `LANG` and two git settings set).

The rows `win_venv`, `linux_attempt1_no_venv` and `linux_system_python` are the outsider route for v2.2, run from the published gist itself after it went public: a clone of the
gist, a full `git clone` of covenant, packages from pip in a new venv on Windows. `linux_attempt1_no_venv` stopped
at exit 2 (no `python3-venv`, so no flask or cryptography in the venv; the packet named the fix); the same clone then
ran with the system Python. An earlier Windows attempt used `py`, which this PC does not have, and never reached the
packet (kept in the record, not in this table). In the Windows gist checkout, line endings were converted to CRLF, so
`run_packet.py` hashed `e9b42e77...` there. `git hash-object` gives `f365ce87...` in both checkouts (README section 4).

v1 had 5 cases and 7 variants. v2 to v2.3 have 14 cases and 11 variants. `v2.0_run1_harness_defect` is the run that failed on
two Windows-only harness defects (`CHANGES.md`). In that run every marker, read count and swap matched the
pre-registration. v2.4 has 15 cases and 12 variants. Its runs 1 and 3 found two defects in the harness, not in
covenant: a case-10 fixture the screen refuses (`getattr`), and the POSIX reading of the new `no_isolation` launch
(`CHANGES.md`); expected outcomes did not change. The run printed below is v2.4 run 4; `run_packet.py` sha256
`a694ccc3cc9775cf73ccbdf1f81948084cce5279876b9ba391a92466b3ccdb09` as run, git blob `c008b520...`.

## The v2.4 Windows run (run 4), as printed (local paths replaced)

```
signed-RUN reproduction packet v2.4 -- covenant ead187b2513fba7bce1404cf3678ae128f38b1b8
python 3.12.10 on Windows-11-10.0.26200-SP0; flask 3.1.3, werkzeug 3.1.8, cryptography 43.0.3
run_packet.py sha256 a694ccc3cc9775cf73ccbdf1f81948084cce5279876b9ba391a92466b3ccdb09; expected.json sha256 c6e0cf906f3a22c96a629400144fa1bed2bc94ea3e5738ec7340fbd7cc8aede4
source: git object store of <local path> (git cat-file blob ead187b2513f:FILE); the working tree was not read; all 9 files match their pinned blob hashes
temporary folder: <local path>

variant pinned               AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant always_refuse        AS PRE-REGISTERED
  1_signed_no_args                ok    NOTHING          reads=1 launches=0 args=-
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    NOTHING          reads=1 launches=0 args=-
  5b_swap_continuous              ok    NOTHING          reads=1 launches=0 args=-
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    NOTHING          reads=1 launches=0 args=-
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant accept_everything    AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    RAN_CHANGED      reads=1 launches=1 args=[]
  2b_one_byte_added               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  3_added_args                    ok    RAN_APPROVED     reads=1 launches=1 args=['--extra', '1']
  3b_one_argument                 ok    RAN_APPROVED     reads=1 launches=1 args=['x']
  4_unsigned_loopback             ok    RAN_APPROVED     reads=1 launches=1 args=[]
  4b_unsigned_tailnet             ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5a_swap_at_launch               ok    RAN_SUBSTITUTE   reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_SUBSTITUTE   reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    RAN_APPROVED     reads=1 launches=1 args=[]
  7_bad_signature_registered_key  ok    RAN_APPROVED     reads=1 launches=1 args=[]
  8_unregistered_key              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  9_signed_without_hash           ok    RAN_APPROVED     reads=1 launches=1 args=[]
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    RAN_APPROVED     reads=1 launches=1 args=[]

variant no_signature_check   AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    RAN_APPROVED     reads=1 launches=1 args=[]
  4b_unsigned_tailnet             ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    RAN_APPROVED     reads=1 launches=1 args=[]
  7_bad_signature_registered_key  ok    RAN_APPROVED     reads=1 launches=1 args=[]
  8_unregistered_key              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    RAN_APPROVED     reads=1 launches=1 args=[]

variant no_hash_check        AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    RAN_CHANGED      reads=1 launches=1 args=[]
  2b_one_byte_added               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    RAN_APPROVED     reads=1 launches=1 args=[]
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant no_args_check        AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    RAN_APPROVED     reads=1 launches=1 args=['--extra', '1']
  3b_one_argument                 ok    RAN_APPROVED     reads=1 launches=1 args=['x']
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant child_reopens        AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_SUBSTITUTE   reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_SUBSTITUTE   reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant extra_parent_read    AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=2 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=2 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=2 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=2 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant no_body_digest       AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    RAN_APPROVED     reads=1 launches=1 args=[]
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant no_signature_verify  AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    RAN_APPROVED     reads=1 launches=1 args=[]
  7_bad_signature_registered_key  ok    RAN_APPROVED     reads=1 launches=1 args=[]
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-

variant no_registry_check    AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    RAN_APPROVED     reads=1 launches=1 args=[]

variant no_isolation         AS PRE-REGISTERED
  1_signed_no_args                ok    RAN_APPROVED     reads=1 launches=1 args=[]
  2_changed_bytes                 ok    NOTHING          reads=1 launches=0 args=-
  2b_one_byte_added               ok    NOTHING          reads=1 launches=0 args=-
  3_added_args                    ok    NOTHING          reads=1 launches=0 args=-
  3b_one_argument                 ok    NOTHING          reads=1 launches=0 args=-
  4_unsigned_loopback             ok    NOTHING          reads=1 launches=0 args=-
  4b_unsigned_tailnet             ok    NOTHING          reads=1 launches=0 args=-
  5a_swap_at_launch               ok    RAN_APPROVED     reads=1 launches=1 args=[]
  5b_swap_continuous              ok    RAN_APPROVED     reads=1 launches=1 args=[]
  6_body_changed_after_signing    ok    NOTHING          reads=1 launches=0 args=-
  7_bad_signature_registered_key  ok    NOTHING          reads=1 launches=0 args=-
  8_unregistered_key              ok    NOTHING          reads=1 launches=0 args=-
  9_signed_without_hash           ok    NOTHING          reads=1 launches=0 args=-
  10_planted_json                 ok    RAN_APPROVED     reads=1 launches=1 args=[]
  C1_ally_key_default_scope       ok    NOTHING          reads=1 launches=0 args=-
removed the temporary folder

RESULT: ALL AS PRE-REGISTERED -- 12 of 12 variants; 25.8 s; exit 0
record: <local path>
```
