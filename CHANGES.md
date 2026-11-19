# Versions of the signed-RUN packet, and why each changed

Nothing is overwritten. Each version is in git as committed, and its runs are kept under `runs/`.

## v1, collective commit 024cb2f (pre-registered), docs in 4096a61

Five cases (case 5 in two forms), seven variants, judged by marker files and the count of child processes. In
`packet/`. Four internal runs (Windows x3, WSL Linux x1): 7 of 7 as pre-registered, exit 0
(`runs/2026-11-17-internal/`).

**Drafted and corrected before it was committed, kept here as written.** In the first draft of `expected.json`, cases
5a and 5b had `"swap_must_occur": true` and this pass rule: "the SUBSTITUTE script did not run, the swap is confirmed
to have happened (probe.py on disk is SUBSTITUTE afterwards), and either the APPROVED script ran in exactly 1 child or
nothing ran and no child started." Before commit 024cb2f, and before any run, it became "swap must occur when a child
was started". The reason: a version that refuses everything never reaches the launch the 5a swap is tied to, so the
draft would have failed it on 5a for a swap that could not happen, not for anything it ran.

**Why v1 was not sent.** ChatGPT's review (`review/CHATGPT_REVIEW_OF_V1_2026-11-17.md`) found three blocking gaps:
- no case binds the signature to the body;
- case 5 does not count reads, and "approved ran" on the pinned code was printed but not enforced;
- the invitation's "every file is small" does not hold for the covenant code (retraction SRP-SMALL-1).
v1 stays in `packet/` as it was.

## v2, collective commit 30d6425 (pre-registered before any v2 run)

`packet-v2/`. 14 cases x 11 variants, each pre-registered as a full observation: an outcome (RAN_APPROVED /
RAN_CHANGED / RAN_SUBSTITUTE / NOTHING / LAUNCH_NO_MARKER / INCONCLUSIVE), the number of times the parent opened the
script, and the child's arguments. What each new case and break answers is in `READINESS.md`.

**v2's first run failed on two harness defects, both on Windows** (`runs/2026-11-17-internal-v2/v2.0_run1_harness_defect/`,
exit 3, 1 of 11 variants as pre-registered):
1. On Windows the `subprocess.Popen` audit event carries the command line as one string (subprocess has already joined
   the list), not a list. v2 read only a list, so every launch's arguments came out as "unrecognized".
2. v2 ordered "swap" before "launch" with `time.monotonic()`. Its resolution on Windows is 0.015625 s (measured:
   `GetTickCount64()`), so the two read as simultaneous and every swap case was INCONCLUSIVE.

In that run every marker file, read count and swap count was what `expected.json` predicted. Only the two readings
above were wrong.

## v2.1: the two readings fixed; expected.json unchanged

- Event order comes from one counter (`itertools.count`) shared by the swap and the audit hook, not from a clock.
- `launch_args()` reads the child's arguments from either form: the POSIX list, or the Windows command line (it finds
  `list2cmdline([workshop, "probe.py"])` in the string and splits what follows).
- `PACKET_VERSION` is "v2.1". `expected.json` is v2's, byte for byte.

## v2.2: DeepSeek's review of v2.1; expected.json unchanged

DeepSeek reviewed v2.1 (`review/DEEPSEEK_REVIEW_OF_V2_1_2026-11-17.md`). It found nothing blocking and seven minor
points. ChatGPT could not be asked: the attachment failed to upload to its chat, three times. Taken:
- `run_packet.py`: a marker with no launch attempt is INCONCLUSIVE, so RAN_* now means what `expected.json` says
  ("after at least one launch attempt").
- `run_packet.py`: a missing or unreadable `expected.json`, or an output folder that cannot be made, is exit 2 with a
  plain message instead of a traceback.
- README: the RAN_* bullet states the launch condition; a note on reading LAUNCH_NO_MARKER where a run was expected;
  the `python3-venv` fallback.
- CLAIM: "no ally is registered on the owner's PC" becomes what was actually checked (a directory listing of his
  covenant folder that day; other machines not checked).

Not taken, with the reason:
- Classifying LAUNCH_NO_MARKER on a positive case as INCONCLUSIVE. A broken guard can produce it too (v1's Windows
  `child_reopens` 5b did), so it stays a difference (exit 1), and the README now says how to tell the two apart.
- Replacing 5b's pre-registered RAN_SUBSTITUTE-or-LAUNCH_NO_MARKER under `child_reopens` and `accept_everything` with
  per-platform expectations. 5a requires RAN_SUBSTITUTE under both, deterministically, so the child-reopen break is
  still caught on every platform. The 5b disjunction was written down before any v2 run, from v1's Windows result.

## v2.2, publication edit (2026-11-17, on Lawrence's "get this done, or at least functional")

The packet goes out as a public gist, a flat folder, so README and REVIEWER_RETURN could no longer point to
`../review/` and `../runs/`, which are in this private repository. They now name files published beside them: the
two reviews (copies with the chat links removed and the full name shortened, each saying so at its top), this
CHANGES.md, and `RUNS_SUMMARY.md`, built from the raw run records by `publish/build_publish.py`. README also says
which two files are needed to run. `run_packet.py` and `expected.json` are byte-identical to `5b4fcf8`, so every v2.2
run above still describes the published code. `expected.json`'s "what" field still mentions `../packet/` and
`../review/`. It is pre-registered and left as written.

## Published, then the outsider route run from the gist (2026-11-17)

Public gist https://gist.github.com/LAWLESS1987/79d125f515a2a90556acbde557ae9c57, first revision `4a694abf`, made from
commit `6b9f113`. All nine files read back identical to what was sent. Then the gist was cloned and run the way an
outsider would (`runs/2026-11-17-gist-route/`):
- Windows, the gist cloned with a full `git clone` of covenant: the first attempt used `py`, which this PC does not
  have, and never reached the packet. With `python -m venv` and pip (cryptography 50.0.2, werkzeug 3.1.9, newer than
  any we had tested), 11 of 11, exit 0, 43.1 s.
- Ubuntu on WSL2: `python3 -m venv` failed (no `python3-venv`), and the packet stopped at exit 2, naming the install
  command. With the system Python, 11 of 11, exit 0, 17.9 s.
- **Found:** Git for Windows converted the gist's line endings to CRLF on clone, so the printed sha256 of
  `run_packet.py` was `e9b42e77...`, not ours. README section 4 now gives `git hash-object` values, which match in
  both checkouts (measured), and adds these runs to its tested table. `run_packet.py` and `expected.json` unchanged.

**Pushed red, then fixed.** Commits `6b9f113` and `3dd49c7` were pushed with research_grade at 61/63. R1 found the
withdrawn SRP-SMALL-1 wording, uncited, in the publication copies of the two reviews (`publish/`). My earlier 65/65
ran before those files were tracked, so it had not read them, and the second time the check ran in the same command
as the push and did not stop it. The copies are verbatim review records, so the retraction now allows those two files
by name, as it already allows `review/`. R1 was re-driven: a probe in `publish/` restating the wording still turns R1
red (61/63), and with the probe retired it is green (65/65). From here, a push goes only after a green research_grade.

## v2.3: one fixture address replaced (2026-11-17, on Lawrence's "Fix it if it's a security flaw.")

The published v2.2 used an address from the 100.64.0.x block our own tailnet assigns from as case 4b's "unsigned
caller from the tailnet". It could not be confirmed that it is not a real node's, so it was
treated as a disclosure and replaced by `100.127.255.254`, the last address of `100.64.0.0/10`. Covenant at the pin
treats every address in `100.64.0.0/10` as tailnet (`TAILNET_CGNAT` in `covenant_unified_v8.py`), so case 4b tests the
same thing. Changed: that one address in `run_packet.py`, its mention in `expected.json`'s "what" text and in
README's case table, `PACKET_VERSION` and the version line. No expected outcome changed. `expected.json` is no
longer v2's byte for byte, because its description text changed; its outcomes are.

Runs, from clean copies against covenant `9d85f6c`: Windows 11, Python 3.12.10, 11 of 11 as pre-registered, exit 0,
24.3 s (`runs/2026-11-17-internal-v2/v2.3_run1/`); Ubuntu on WSL2, Python 3.14.4, 11 of 11, exit 0, 8.4 s
(`v2.3_run2_wsl/`).

v2.3 `run_packet.py` sha256 `848f3b8642e3e0e67989ecb43ba91e52f8b6ae5fa2481cb1e14b833efaed7310` (git blob `03214394055e3eb4c3622b82c4a92eb8dadc24fd`); `expected.json` sha256 `192e14dd28cc1bea00318694e6273b30e426915e476b380ae214e021ce23d0d0` (git blob `01b97e9e3fc5c6f0b7275bbba532171b0957f9e1`).

The gist's earlier revisions (`4a694abf`, `7f21060a`) still contain the old address in their public history; only
deleting the gist would remove them, and it was not deleted.

## v2.4: the new pin, capitaharlock's case, nootxlm's three points (2026-11-18, on Lawrence's "So do it.")

**Why.** v2.3 pinned `9d85f6c`. Since then three changes reached covenant's public `main`: A447 (#78) makes the door's
RUN check accept only one of the operator's own registered keys, which closes what case C1 showed; A446 (#80) makes a
refused RUN's text state that rule (Jang-woo, HF 183807 #44, found it still said loopback was enough); A444 (#76) makes
the signed-request nonce store durable across processes. Promised in our posts: C1 re-run at a pin with the ally fix
(HF 180706 #40), capitaharlock's planted-`json.py` case and its control (HF 191990 #3), and nootxlm's three points on
v2.3 (180706 #40): the import-time `Popen` patch, the citation one line too wide, and scope in the first sentence.

**Pre-registered before any v2.4 run** (this commit; the gist's history shows the order):
- Pin `ead187b2513fba7bce1404cf3678ae128f38b1b8`. Nine files: `pairstore_excl.py` joins the eight, because the durable nonce store imports it when a
  case first checks a nonce. Its git blob hashes are read from git at the pin by `v24_pin.py`, never typed.
- C1: expected NOTHING, one read (it ran at `9d85f6c`). Its breaks: `no_signature_check`, `accept_everything` and
  `no_registry_check` are expected to run it (the last because an unregistered key then passes as an operator; read
  from `verify_signed` at the pin); `extra_parent_read` no longer expects a second read in C1, which no longer reaches
  `run()`.
- New case `10_planted_json`: the approved script imports `json` and writes the approved marker; `json.py` planted
  beside it writes `ran_planted.txt` if imported. Expected: RAN_APPROVED, one read, no child arguments, the planted
  file not loaded. New observation `planted_loaded`.
- New break `no_isolation`: the launch without `-I`. Expected: the planted file loads in case 10; nothing else changes.
- `always_refuse` expects case 10 to launch nothing; `extra_parent_read` expects two reads in case 10.
- Harness: `COVENANT_NONCE_STORE` points into the run's temporary root; the list of files loaded from the source
  folder is taken after the cases, so a lazy import is listed too.

**Docs.** README opens with the scope; the import-time `Popen` patch is described (README section 2, CLAIM.md);
the key-generation and signed-message ranges are measured from the syntax tree at the pin, which corrects v2.3's
one-line-wide ends (2009 for 2008, in both); outside runs of v2.3 by nootxlm and Jang-woo are linked;
`REVIEWER_RETURN.md`'s heading said v2.1 in v2.2 and v2.3 and now says v2.4.

**Runs** (`runs/2026-11-18-internal-v2.4/`), each from a clean copy of the two packet files, against `ead187b`:
- **Run 1, Windows: exit 1, 1 of 12.** Every difference was case 10, in every variant but `always_refuse`: nothing
  launched. The screen refused the fixture script, which printed `getattr(json, "PLANTED", ...)`, and the screen
  refuses the name `getattr`. Every other cell matched, C1 included. A defect in our fixture, not in covenant. The
  script now ends `print("approved bytes ran")`; the planted marker already says whether `json.py` loaded. Expected
  outcomes unchanged. (Collective commit `5f6bd61` says in its message that the fixture was fixed; the edit had
  failed and only the run was committed. The fix is `15017a0`.)
- **Run 2, Windows: 12 of 12, exit 0, 26.7 s.**
- **Run 3, WSL: exit 1, 11 of 12.** Only `no_isolation` differed: on POSIX the harness read its launches as
  `<unrecognized launch>`, because `launch_args` assumed `-c` at index 2 and the break drops `-I`. A defect in our new
  break's reading, not in covenant; Windows parses the joined command line and was not affected. Fixed to find `-c`
  where it is (`09c5ecf`); expected outcomes unchanged.
- **Run 4, Windows, and run 5, WSL, on that harness: 12 of 12, exit 0** (25.8 s; 9.2 s). Pinned: C1 refused with the
  A446 text; case 10 ran the approved bytes and the planted file did not load; in `no_isolation` it loaded. All nine
  files listed as loaded, `pairstore_excl.py` included; no socket event, no write outside the run's folder.

v2.4 `run_packet.py` git blob `c008b5203d1ca852e152b7dd3a9b76bfc4f3862b` (sha256 as run
`a694ccc3cc9775cf73ccbdf1f81948084cce5279876b9ba391a92466b3ccdb09`); `expected.json` git blob
`4fdb71c207ead8e785fd2723b5ce8a7b00357608` (sha256 `c6e0cf906f3a22c96a629400144fa1bed2bc94ea3e5738ec7340fbd7cc8aede4`),
unchanged since its pre-registration commit `0b78fc3`.

**Published 2026-11-18** to the same gist (https://gist.github.com/LAWLESS1987/79d125f515a2a90556acbde557ae9c57) as two
revisions: `226391a` holds the pre-registration as committed in `0b78fc3`, and `360bf3a` the files after the runs
(`b65e880`). All nine files read back blob-identical to `b65e880`. Outsider route on Windows: the gist cloned, a fresh
`git clone` of covenant from GitHub, 12 of 12, exit 0, 25.4 s (`runs/2026-11-18-gist-route-v2.4/win_clone/`).

## v2.4, README and records only (2026-11-19, on Lawrence's "go"); `run_packet.py` and `expected.json` unchanged

**Why.** capitaharlock (HF 191990 #7) noted that the full case 10 was the one open item on Python 3.10 and 3.11.
Jang-woo (HF 183807 #47) posted his v2.3 return files in a gist with a `SHA256SUMS.txt`. Our replies (191990 #8,
183807 #48) said the README still listed 3.10/3.11 as untested and that the gist link would wait for the next publish.

**Run 6, WSL** (`runs/2026-11-18-internal-v2.4/v2.4_run6_wsl_py3.10.21/`, `..._py3.11.16/`, script
`v2.4_run6_wsl_py3.10_3.11.sh`): the published LF bytes of the two packet files (`run_packet.py` sha256
`380e91f2...`, git blob `c008b520...`; `expected.json` git blob `4fdb71c2...`), uv's Python 3.10.21 and 3.11.16, a new
venv each with only flask and cryptography installed by uv (flask 3.1.3, werkzeug 3.1.9, cryptography 50.0.2), the
run under `unshare -rn` and `env -i`. Both: 12 of 12, exit 0 (10.2 s; 9.2 s); all nine covenant files matched their
pinned blob hashes; case 10 as pre-registered both ways (planted `json.py` not loaded under the pin, loaded under
`no_isolation`).

**README.** Section 4's v2.4 table gains the two run-6 rows and the v2.4 outsider-route row (`win_clone`, measured
2026-11-18 but missing from the table), with a paragraph on how run 6 was made. "Not tested by us" no longer names
3.10 or 3.11 and says instead "Python versions not in these tables". Section 8's line on 3.10/3.11 for case 10 now
reads as Python versions we have not run (its note that `-I` also implies `-P` went with it). The top links Jang-woo's
gist at revision `b48a49c7`, says what we checked in it and that we did not run his extra cases, and says the README
was revised on 2026-11-19 with the packet files unchanged. Nothing else changed.

**Records.** `RUNS_SUMMARY.md` (rebuilt by `build_publish.py`) gains the run-6 and `win_clone` rows.
`runs/2026-11-18-jangwoo-v2.3-gist/FETCHED.md` gets a correction below its original text: its check said the packet
he ran is the one we published, but only `run_packet.py` and `expected.json` were matched.

Not changed: our byte-for-byte copy of Jang-woo's files stays in the collective's private record and is not
published beside the packet; his gist is linked instead.

Reviewed before publishing by Cael, Cipher, Gemini and ChatGPT (`review/README_UPDATE_2026-11-19.md`, private).
**Published 2026-11-19** on Lawrence's "Yes, publish" to the same gist as revision `0d91c938`, from collective commit
`7acb314`: only `README.md`, `CHANGES.md` and `RUNS_SUMMARY.md` changed, and all nine files read back equal to
`7acb314`. The gist was first checked to equal the v2.4 publish (`b65e880`, revision `360bf3a`).
