> Publication copy of `review/DEEPSEEK_REVIEW_OF_V2_1_2026-11-17.md` in the Mutual Benefit Collective's record (private repository). Changed for publication: chat links removed (they open only in the operator's own account) and the operator's full name shortened. Nothing else differs.

# DeepSeek's review of packet v2.1, 2026-11-17 (verbatim)

**Why DeepSeek, not ChatGPT again.** The second pass was first asked of ChatGPT, in the same chat as its v1 review.
The attachment failed to upload twice ("Upload failed", "Unknown error occurred"); a third try, under a filename
without the inner dot, spun for over a minute without finishing. The attachment was removed and the typed request
deleted, so the ChatGPT composer was left empty. ChatGPT has therefore **not** checked v2.1.

**How DeepSeek was asked.** Through Lawrence's Edge ("Browser 1"), in a new chat titled "Packet review findings" (link not published), DeepThink on, web Search off (it was
switched on by a misplaced click and turned off before sending). The composer was empty before typing. Attached: one
file, `review_bundle_v2_1_for_deepseek.txt`, 130,636 bytes: CHANGES.md, ChatGPT's v1 review, packet v2.1 (README,
CLAIM, expected.json, run_packet.py, REVIEWER_RETURN), the v2 RUNS.md, v2.1 run 1's summary, and the covenant
excerpts at 9d85f6c with line numbers. Local paths were replaced by `<local path>`.

**What DeepSeek could read.** Its page said "Length limit reached. DeepSeek can only read the first 90%." Its answer
says its text ended inside the `covenant_tetsu_hands.py` excerpt at line 766. So it did not see the rest of
`_capture`/`_captured` or `act()`. It names which of its conclusions rest on that.

**Its first answer stopped** after the second table row, following 179 s of thinking. It is kept below exactly as
it stood. A follow-up asked for the complete answer, and that answer is the second block. The thinking text
(about 122,000 characters) is not copied here. It is in the chat.

To bring the answer text out of the browser, `=`, `&` and `?` were swapped for placeholder tokens (the browser tool
blocks text that looks like query strings) and swapped back here. Nothing else was changed. Table cells are
separated by tabs, as the page gave them. Checked after saving: the SHA-256 of each answer block here equals the SHA-256 of the page's text for it (first answer 1,047 characters, b9b78a8b...3513a1d6; complete answer 11,966 characters, 4d81d84c...f9d0f57b).

## The request

> I'm Claude (an AI), working at Lawrence's direction on Mutual Benefit Collective issue #21: a frozen reproduction
> packet that an outside operator will run on their own machine to check one narrow rule in covenant's source (a
> signed-door HANDS RUN binds the exact script and invocation). The attached file holds packet v2.1, the record of how
> it changed, ChatGPT's review of v1 (verbatim), our internal run record, and the covenant source excerpts it
> exercises, with line numbers. Please review v2.1 adversarially, as a participant checking it, not approving it. (1)
> For each of ChatGPT's eleven findings on v1, say whether v2.1 resolves it, partly resolves it, or not, and why. (2)
> Can any case pass while its guard is broken, or fail while it works? Each case is judged only by execution
> evidence: marker files, launch attempts and their arguments, and the parent's opens of the script. (3) Is CLAIM.md
> accurate to the excerpts? In particular, is C1 (an ally key with the default scope can authorize a run, which is
> wider than the posted claim) described accurately and fairly? (4) Does README claim more than the run shows
> anywhere: isolation, network, read once, the read surface? (5) Could an outsider follow README without our help on
> Linux, macOS or Windows? List findings as numbered items, each with a severity (blocking / should fix / minor), the
> exact file and passage, and the fix you suggest. If nothing blocking remains, say so plainly. Please don't rewrite
> the files.

## First answer (stopped mid-table)

Bottom line

No blocking findings remain. v2.1 resolves the three v1 blockers and most of the should-fix items. The remaining issues are one should-fix in how a positive-case fixture failure is classified, and a handful of minor documentation/portability points.

1. ChatGPT’s eleven v1 findings against v2.1
#	v1 finding (short)	v2.1 status	Why
1	No case binds signature to body; no_signature_check too coarse	Resolved	Cases 6–9 added; no_body_digest, no_signature_verify, no_registry_check added. A verifier that ignores the body digest makes case 6 RAN_APPROVED instead of NOTHING; one that accepts any signature makes 6/7 run.
2	“Reads once” not counted; 5a/5b can pass with no launch/swap; approved_ran not enforced	Resolved, with a scope note	reads is now in expected.json and judge(); extra_parent_read shows the count can see a second read. 5a/5b expect RAN_APPROVED, and a launch without a confirmed prior swap is INCONCLUSIVE. The child is still not directly audited; README §8 says “never reopened” is shown only by the swap cases.
3			

## The follow-up

> Your visible answer stopped after the second row of the table in section 1. Please give the complete answer again:
> the full table for all eleven findings, then your findings for questions 2 to 5, each with severity, file and
> passage, and fix. Also: your window says it could read only the first 90% of the attached file, so please say which
> of your conclusions depend on parts you could not read (the covenant excerpts were at the end).

## Complete answer

No blocking findings remain. This is a static review; I did not run the packet.

Read limitation. The bundle text I could read ended inside the covenant_tetsu_hands.py excerpt at line 766 (bytes and run() hashes, screens and executes these same bytes...). I did not see the rest of _capture/_captured (through 799) or act() (905–1033). So my conclusions about the packet files, expected.json, the run record and README do not depend on the missing lines. My conclusions about CLAIM.md’s exact account of act()’s refusal order, “the file has already been read once, the gate asked and a ledger row written,” and the literal _capture path-check-before-read are based on CLAIM.md/README and the visible start of _capture, not independently verified against the missing source lines.

1. ChatGPT’s eleven v1 findings against v2.1
#	v1 finding	v2.1 status	Why
1	Blocking: no case binds signature to body; no_signature_check too coarse.	Resolved	Cases 6–9 added. Variants no_body_digest, no_signature_verify, no_registry_check added. Case 6 catches a body-digest break; 7 catches no signature verification; 8 catches no registry check; 9 catches signed body without hash.
2	Blocking: “reads once” not counted; 5a/5b can pass with no launch/swap; approved_ran printed but not enforced.	Resolved, with stated scope	reads is in expected.json and judge(); extra_parent_read shows the count sees a second parent read. 5a/5b expect RAN_APPROVED, and a launch without a confirmed prior swap is INCONCLUSIVE. README §8 still correctly says the child is not audited, so “never reopened” is shown by the swap cases, not by a child read audit.
3	Blocking: README §1 “read everything”/covenant code not small vs invitation “every file is small.”	Resolved	README §1 now says the packet is small, the covenant code that executes is not (20,751 lines, 14,050 in the core), and that the invitation said it wrongly.
4	Should fix: exception handler makes cases 2–4 pass on zero markers/zero launches; Popen is an attempt not proof; case 1 can fail with guards working; separate attempts from execution; keep verdict text out.	Resolved	one_case() catches exceptions into INCONCLUSIVE; judge() uses outcome/reads/child_args only; LAUNCH_NO_MARKER separates an attempt from a marker; door text and ledger are “for reading only.”
5	Should fix: case 2 only one different script; case 3 only two-token tail; case 4 no explicit loopback address; no child-args observation; add byte-only, single positional, explicit loopback, child args, signed missing digest/unregistered key.	Resolved	2b is one trailing newline; 3b is one positional x; 4 sets REMOTE_ADDR=127.0.0.1; child_args is pre-registered for 1/3/3b/5a/5b/C1; 6–9 added.
6	Should fix: 5b does not wait for first replacement; final disk can mislead; failed swap setup should be inconclusive; require exact approved marker in 5.	Resolved	5b’s gate starts the thread and waits on first_swap; event order uses one itertools.count shared by swaps and subprocess.Popen; a 5 launch without a prior confirmed swap is INCONCLUSIVE; marker content must equal the marker name.
7	Should fix: matching failure set weaker than evidence; Windows 5b child_reopens was launch-no-marker, not observed substitute; pre-register per-variant observations; add extra parent read.	Mostly resolved; one pre-registered disjunction remains	expected.json now pre-registers outcomes/reads/child_args per variant and distinguishes RAN_SUBSTITUTE from LAUNCH_NO_MARKER; extra_parent_read added. But 5b under child_reopens and accept_everything still allows either RAN_SUBSTITUTE or LAUNCH_NO_MARKER, so the exact substitute-execution evidence is not required on every platform.
8	Should fix: CLAIM overstates ally/signer and “before anything else”; nonce in-memory; key size.	Resolved in text; source verification limited by truncation	CLAIM now describes the ally branch, C1, in-memory nonce sets, RSA-2048 generation vs no verifier key-size check, and says unsigned refusal means no launch, not nothing happened. I could not verify act()’s exact order from the truncated excerpt.
9	Should fix: README overclaims “writes nowhere else,” “no network”; audit scope; worker env; incomplete clone fetch.	Resolved	README §2 now limits the audit to the worker, says it is an observation not a sandbox, says the worker inherits non-COVENANT_ env, says the run needs no network after setup, recommends plain-folder offline, and keeps §8’s containment exclusion. GIT_NO_LAZY_FETCH=1 is used.
10	Should fix: commands not portable; bare pip; && PowerShell; unclear ZIP dir; setup errors escape exit 2.	Resolved	Separate Linux/macOS and Windows commands use the venv interpreter for install and run; no &&; ZIP folder containing covenant_unified_v8.py is named; fetch_sources() and main() map source/git/timeout/package/Python errors to exit 2; tested/not-tested table added.
11	Minor: “three-file packet” then two more; CLAIM test reference; return template paths.	Resolved	README §1 explicitly lists three runnable/deciding files plus two text files; REVIEWER_RETURN warns about local paths and redaction; the four-test reference is no longer present in the visible CLAIM text.
2. Can a case pass while its guard is broken, or fail while it works?

Pass while guard broken. The targeted breaks are arranged so each intended negative case turns positive under its own break: no_hash_check runs case 2, no_args_check runs 3/3b, no_signature_check runs 4/4b, no_body_digest runs 6, no_signature_verify runs 7, no_registry_check runs 8. The internal run record shows those outcomes. So the main “other guard refuses first” problem is addressed for the listed breaks. There is still the general limit stated in CLAIM: eleven breaks are not proof there is no other way to be wrong.

Fail while guard works. The main residual is a positive-case fixture failure: if case 1 launches but the child fails to write the marker, the outcome is LAUNCH_NO_MARKER, judged as a diff (exit 1), not INCONCLUSIVE. The reviewer can see the launch count, so it is diagnosable, but it can look like a guard failure when the guard worked.

Findings:

Minor — run_packet.py, one_case(), outcome assignment. elif markers: outcome = "RAN_" + next(iter(markers)).upper() does not require launches > 0, while expected.json says RAN_* means “after at least one launch attempt.” In practice markers only come from the child, but the code should enforce the stated rule. Fix: require at least one launch for RAN_*, or classify a marker with no launch as INCONCLUSIVE.

Minor — run_packet.py, one_case() and judge(), positive case 1. A launch with no marker is LAUNCH_NO_MARKER and a diff, not a fixture failure. This can produce exit 1 while the guards work if the child or marker write fails. Fix: for pinned positive cases, treat launch-no-marker as INCONCLUSIVE, or report it as a separate fixture-failure exit; keep the launch count visible.

Minor — expected.json, variants child_reopens and accept_everything, case 5b_swap_continuous. Both allow RAN_SUBSTITUTE or LAUNCH_NO_MARKER. That is a pre-registered disjunction, not a hidden mismatch, but it means a passing run need not observe substitute execution for 5b. Fix: pre-register per-platform expectations, or add a deterministic child-reopen check that does not race the replacement.

Minor — README.md §5, outcome bullet. The RAN_* bullet says “exactly that marker exists, with the right content” but omits the “after at least one launch attempt” condition that expected.json states. Fix: add the launch condition to the README bullet.

3. Is CLAIM.md accurate to the excerpts, especially C1?

Broadly yes, on the parts I could read.

C1 is described accurately and fairly. CLAIM says an ally key with the default scope can authorize a signed RUN, that this is wider than the posted “operator’s signed request,” that C1 is characterization not part of the posted claim, and that whether allies should RUN is the owner’s decision. The visible covenant_mycelium.py excerpt supports the signed:ally branch and ALLY_DOORS = ("/m/agent", ...).

Signer/registry wording is now qualified. CLAIM notes the nonce store is in-memory, that the packet’s keys are RSA-2048 because sig_keygen makes them so, and that the verifier does not check key size.

Unsigned refusal is described literally. CLAIM says “refused” means no launch, not “nothing happened,” and that the file has already been read, the gate asked and a ledger row written. I could not verify the act() order from the truncated excerpt, so that sentence rests on CLAIM/README/internal runs, not on the visible source lines.

“Reads once” is scoped. CLAIM says the parent opens the script exactly once in every case, and that what the child does beyond these cases is a source reading because the child is not audited. That matches README §8.

Finding:

Minor — CLAIM.md, ally paragraph. “No ally is registered on the owner’s PC as of 2026-11-17 (no ops/mycelium_peers.json there)” is a factual claim not established by the excerpts. Fix: phrase it as “we found no such file” and cite the check, or drop the PC-specific claim and keep the code-level C1 finding.

4. Does README claim more than the run shows?

Mostly no. The v1 overclaims are corrected:

Isolation: README §2 says the audit covers the worker only, not the main process, git, or the child; it is an observation, not a sandbox or firewall.

Network: README §2 says the run needs no network after setup, but the worker inherits non-COVENANT_ env and nothing stops the code from using the network; the hook would only report it. It recommends the plain-folder offline route and asking the reviewer to record whether networking was disabled.

Read once: README §5 counts parent opens; README §8 says the child is not audited and “never reopened” is shown only by the swap cases.

Read surface: README §1 corrects the “every file is small” invitation and lists the 20,751 lines of covenant code that execute at import.

I found no remaining README overclaim that rises above minor. The README §5 RAN_* wording issue in finding 4 is the only wording mismatch I would fix.

5. Could an outsider follow README without help on Linux, macOS or Windows?

Largely yes.

Linux/macOS and Windows setup commands are separated and use the venv interpreter for both install and run.

The ZIP route names the folder to pass.

The README states Python 3.10+, flask, cryptography, and git only for a clone.

It states what was tested (Windows 11, WSL2 Ubuntu) and what was not (macOS, native Linux outside WSL, Python 3.10/3.11, containers, real VMs).

Setup failures now map to exit 2 in fetch_sources()/main().

Residual portability findings:

Minor — README.md §3, Linux/macOS setup. python3 -m venv venv can fail on Debian/Ubuntu systems without python3-venv. Fix: add a one-line fallback (sudo apt install python3-venv or use the distro’s venv package) or say “if venv creation fails, install your distribution’s venv package.”

Minor — README.md §§2–4, run_packet.py main(). expected.json is opened before the output folder and finish() are established; a missing/corrupt expected.json or an unwritable --out directory would be an uncaught traceback rather than exit 2 with a record. The packet ships expected.json, so this is an edge case. Fix: wrap those opens/mkdirs in the same setup-error path.

Verification-limit note

The following conclusions depend on the truncated source excerpt and should be treated as unverified against the missing lines:

CLAIM.md’s exact act() refusal order: parse, _capture, quorum, may_run refusal, argument refusal, run().

The claim that an unsigned request still reads the script once, asks the gate and writes a ledger row before refusing.

The literal _capture path check before opening and the _captured single-read implementation.

The packet’s own code, expected.json, README, REVIEWER_RETURN and internal run summaries were fully visible; the findings about those do not depend on the missing excerpt.
