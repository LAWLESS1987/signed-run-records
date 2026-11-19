# Signed-RUN packet: our run records (cleaned copy)

The raw records behind the signed-RUN reproduction packet's `RUNS_SUMMARY.md`: the internal runs in our record of
packet v1 to v2.4, and the outsider-route runs from the published gist. The packet itself is
https://gist.github.com/LAWLESS1987/79d125f515a2a90556acbde557ae9c57; its README says these records were kept in
the Mutual Benefit Collective's private repository. This is a copy of them, made so that anyone can check our
summaries against what the runs printed.

**These are our own runs (internal preparation), not outside reproductions.** Outside runs are linked from the
packet's README and belong to the people who ran them.

Made by Claude (an AI) at Lawrence's direction, by `build_records_extract.py` (included here; see below), from
the collective's commit `99befe973b80ae3fd12f6454e44cc0f8c06dd876`, folder `reviews/signed-run-packet-2026-11-17/`. That repository is
private, so the commit id cannot be checked from outside; it is given so that the copy can be traced back to it.

## What is here

156 files, laid out as in the private record: `runs/` (one folder per run: `environment.json`,
`results.json`, `summary.txt`, `workers_raw.json`, and the console output), `packet/` (v1) and `packet-v2/` (v2.4,
as published), `CHANGES.md` (every version and why it changed), `READINESS.md`, and `publish/` (the files published
beside the packet). `CHANGES.md` and `READINESS.md` mention files that are not here: our internal review drafts
(`review/`), `publish/build_publish.py` (which names what it removes), and our copy of Jang-woo's return (his own
gist is the public copy).

## What was changed

Only what identifies the operator's machine or private network, and one name. Of the 156 record files,
48 are byte-for-byte the originals; in the other 108, exactly these replacements were made (counts
summed over those files):

| what | replaced by | count |
|---|---|---|
| the per-session temporary folder (under `AppData`, `Local`, `Temp`, `claude`: two ids) | `<temp>` | 221 |
| the Windows user folder name (`C:\Users\<name>`) | `<user>` | 894 |
| the WSL home folder name (`/home/<name>`) | `<user>` | 185 |
| an address inside our own tailnet's block: the case-4b fixture address of v2.0 to v2.2, replaced in v2.3 because it sat there | `<withheld tailnet address>` | 198 |
| the operator's surname, in packet v1's README | removed | 1 |

`SANITIZED.json` lists every file with its original's git blob hash, this copy's sha256, and the replacements made
in it. A changed file's hash differs from the private original's, so for those files this copy can be checked
against the rules above, not against the original's hash. Every `.json` file still parses. `packet-v2/run_packet.py`
and `packet-v2/expected.json` are unchanged and have the git blob hashes of the files in the published gist
(`c008b5203d1ca852e152b7dd3a9b76bfc4f3862b` and `4fdb71c207ead8e785fd2723b5ce8a7b00357608`; `git hash-object`
gives them).

Kept on purpose, because a reproduction is checked against them or they are already public: each run's platform
string, Python version and machine type (in `environment.json` and the console output); the loopback address
`127.0.0.1`; the replacement fixture address `100.127.255.254` and the range `100.64.0.0`, both in the published
packet; and the name Tetsu, an AI partner named throughout the public covenant repository.

`build_records_extract.py` is the script that made this copy, with two literals in it redacted: the user folder
name (shown as `<user>`) and the surname (`<surname>`). It reads a git repository, so it cannot be run here; it
shows what was matched and replaced, and the check that stops the build if any of it is left.

## Not checked by this copy

That these records are complete or that the runs happened as recorded: the copy shows what our run records say,
not that they are true. A run on your own machine is the check that does not depend on us.
