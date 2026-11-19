# Issue #21 readiness report: signed-RUN reproduction packet

2026-11-17. By Claude (an AI), who claimed the task on #21 (comment 6954839077). **Internal preparation only: no
outside operator has run it.**

**Update, after Lawrence's "Discernment towards mutual benefit of all intelligence to get this done, or at least
functional":** the branch is pushed, and the packet is public as gist
https://gist.github.com/LAWLESS1987/79d125f515a2a90556acbde557ae9c57. The outsider route (clone the gist, clone
covenant, install, run) was then run from the gist itself: 11 of 11, exit 0, on Windows (new venv, cryptography
50.0.2) and on WSL Linux (`CHANGES.md`, last section). The HF posts are the originating session's. The text below was
written before publishing and is kept as written.

## Status

**Packet v2.2 is ready for an outside run, pending three decisions that are his** (bottom of this page). It is the
folder `packet-v2/` as committed in collective commit `5b4fcf8` on branch `claude/issue-21-signed-run-packet`,
pinned to covenant `9d85f6c902bcfab4616be0d3b08d0715584f7a07` (public `main`, 2026-11-16).

| file | sha256 (bytes as committed, LF) |
|---|---|
| `run_packet.py` (609 lines, the only code) | `e348f5ecc3c20056037f71a4c97f40fc17f5534ffdf32c246b7dcfee7e14b525` |
| `expected.json` (pre-registered at `30d6425`, unchanged since) | `6cd5960bdc87c4ca0fdbdf42bad326da5b0befd61e16c39174533067d59c4538` |
| `README.md` | `9e68f93224c7a4e4baac39eb2717de1780ccbce9f0ab56249d43966af4ac25aa` |
| `CLAIM.md` | `12ebb9955d3ae4ed5238920d22dd51cc8006cc649b7585e293aaddc824cfa05c` |
| `REVIEWER_RETURN.md` | `12dcc3e9bfeb7807f1215a9a541d7ceddf4a99ad8eb5dd4b3349bad978e36839` |

One command after setup: `python run_packet.py --covenant <clone or unpacked zip>`. It needs Python 3.10+, flask and
cryptography. It uses temporary folders and throwaway RSA keys made in memory, and needs no network after setup.

## The claim, checked against the code

`packet-v2/CLAIM.md` has the line-by-line reading. In short, **the code supports the claim as posted**: a signed run
is bound to the SHA-256 of the script's bytes, a signed run with arguments is refused, an unsigned run is refused,
the hash covers the entry file only, and the parent reads the bytes once and hands them to the child on standard
input. Three findings change what the posted words mean:

1. **An ally key can authorize a run (wider than the claim).** The door's check, `_request_signed_by_registered`,
   calls `covenant_mycelium.admit`. `admit` also admits a registered **ally** key on its doors, and the default ally
   scope includes `/m/agent`. So a granted ally with the default scope can sign a RUN exactly as an operator can.
   Case C1 shows it runs. On 2026-11-17 no `ops/mycelium_peers.json` existed in his covenant folder, so no ally was
   registered on this PC; other machines were not checked. Whether allies should be able to RUN is his decision. It
   is not changed here. It looks like a widening nobody chose: A200 (2026-09-21) built ally admission for the
   conversation door, and A423 (2026-11-14) later made RUN depend on that same admission. It is recorded here as a
   finding for covenant, not as a fix.
2. **"Unsigned run is refused" means no launch, not "nothing happened".** The file is read, the gate is asked and a
   ledger row is written before the refusal. It is a property of the `/m/agent` door. The owner's in-process paths
   (the practice loop, the console) run without a signature by design.
3. **"Every file is small, so read it all first" was wrong** for the covenant code the packet loads: eight files,
   20,751 lines, 14,050 of them in the core. The packet itself is small. It is withdrawn as retraction SRP-SMALL-1
   (`docs/RETRACTED.json`). R1 was driven both ways: a probe restating it without the citation went red (61/63), and
   once the probe was retired it was green again (65/65). The correction is owed in both HF threads.

## What was measured (all internal)

Every run used the committed packet files, copied out with `git show`, against a fresh `--depth 1` fetch of the pin.

| version | runs | result |
|---|---|---|
| v1 (5 cases, 7 variants) | Windows x3 (clone, clone, plain folder), WSL Linux x1 | 7 of 7 as pre-registered, exit 0, each run |
| v2.0 (14 cases, 11 variants) | Windows x1 | exit 3: two harness defects on Windows; every marker, read count and swap matched the pre-registration |
| v2.1 | Windows x3, WSL x1 | 11 of 11, exit 0, each run |
| v2.2 | Windows x1, WSL x1 | 11 of 11, exit 0, each run |

Times: Windows 11 / Python 3.12.10, 21.8-23.2 s; Ubuntu on WSL2 / Python 3.14.4, 8.6-8.7 s (v2.x). Covenant's own
tests at the pin: A430 18/18, A430S 13/13, A436 5/5, TH1 31/31. Exit-2 paths driven: a tampered file, a CRLF copy
(v1), an empty folder, a missing `expected.json`. Raw output for all of it is in `runs/`.

**Not measured:** macOS; native Linux outside WSL; Python 3.10 or 3.11; a container or a real VM; the unwritable
output-folder path; anything a running script can do (containment, egress); a deployed node; the HTTP layer; the
rest of the `/m/agent` route; what the child does with its input beyond the swap cases.

## Reviews

- **ChatGPT, v1** (`review/CHATGPT_REVIEW_OF_V1_2026-11-17.md`, verbatim): would not send it. 3 blocking, 7 should-fix,
  1 minor. All eleven were taken into v2. How each was answered is in `CHANGES.md`, and DeepSeek checked them one by one.
- **ChatGPT, v2.1:** not done. The upload failed three times in its chat. Its composer was left empty.
- **DeepSeek, v2.1** (`review/DEEPSEEK_REVIEW_OF_V2_1_2026-11-17.md`, verbatim, hash-checked against the page): "No
  blocking findings remain." On ChatGPT's eleven: nine resolved; #7 mostly resolved (one pre-registered disjunction);
  #8 resolved in text, with source verification limited. DeepSeek could read only 90% of the bundle. It did not see
  `act()` or the end of `_capture`, and it says which conclusions rest on that. Five of its seven minor points were
  taken into v2.2. Two were declined, with reasons, in `CHANGES.md`.
- **Cael (local stock 27B), v2.2:** asked after Lawrence's "have Tetsu and the other models help" (relayed). The
  request is `review/CAEL_REQUEST_2026-11-17.txt` (3,448 characters). No answer: the door timed out after 600.3 s
  (`TimeoutError`, 17:55:58Z), so the RTX box's 27B was not reachable or not serving. Not retried; not counted.
- No reviewer ran the packet. Both reviews are static.

## Against what the HF posts promised (180706 #36, 183807 #42)

| promised | packet v2.2 |
|---|---|
| one pinned commit and one command | yes: covenant 9d85f6c; `run_packet.py --covenant PATH` |
| temporary folders, throwaway keys, no network, none of our credentials | yes; the run needs no network after setup. The audit covers the worker only, and README says so |
| five cases, outcomes written down before running | yes, plus nine more; v1 pre-registered at 024cb2f, v2 at 30d6425, each before its first run |
| a fifth case swapping the file after the check | built two ways (at launch; continuously from the gate); not reduced to a reading of the source |
| checks look at whether the script ran, not verdict text | yes: marker files, launch attempts and arguments, parent reads |
| always-refuse fails case 1; accept-everything fails the rest | yes, plus nine single-guard breaks |
| Python version, dependencies, rough run time | yes (README section 4) |
| "every file is small, so read it all first" | **no: withdrawn (SRP-SMALL-1); README section 1 says so and lists the short path to read** |
| "the operator's signed request" | **narrower than the code: an ally key can also sign (C1)** |

## What needs his word (nothing below has been done)

1. **Push** branch `claude/issue-21-signed-run-packet` to the collective. Then this report and the commit link go on
   #21, as the issue asks.
2. **Publish the packet where outsiders can get it.** The collective repo is private. The likely route is a public
   gist holding the five `packet-v2/` files as committed (hashes above). The packet text names him only as "Lawrence"
   and contains no paths of his. The raw run records in `runs/` do contain local paths, and none of them are needed by
   an outsider.
3. **Post in the two HF threads.** A draft follows, not posted. It has to carry the correction and the ally finding,
   since both change what the posts said.

Also his decision, for covenant (not this task): whether ally keys should be able to authorize a RUN (finding 1). If
not, the narrow fix is for the HANDS door to accept only `signed:operator`. That is a covenant change, with its own
entry and tests.

## Draft for both HF threads (not posted; same text for each, with the first line changed)

> The packet is ready: [gist link], files pinned by SHA-256 in its README, against covenant commit 9d85f6c. One
> command after setup: `python run_packet.py --covenant <your clone>`. Python 3.10+, flask and cryptography. We
> measured about 22 s on Windows and 9 s on Linux.
>
> Two corrections to what we said before. First, our post said every file would be small enough to read first. The
> packet's own files are, but the covenant code it loads is eight files and about 20,700 lines. The README lists the
> short path the claim rests on, by line number. Second, writing the packet turned up that a registered ally key, not
> only the operator's, can authorize a signed run. A case (C1) shows it. Whether that should stay is our operator's
> decision. The claim is otherwise as posted.
>
> It grew from five cases to fourteen after review by ChatGPT and DeepSeek. Both reviews are linked. Every outcome
> was written down before we ran it. A case that comes out differently on your machine is the result we'd most want.
> A no is a fine answer.
>
> -- written by Claude, an AI, posted at Lawrence's direction
