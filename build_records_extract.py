"""Build a cleaned extract of the signed-RUN packet's run records, for a possible public copy (issue #21).

Usage: python -I build_records_extract.py OUT_DIR [REV]     (REV defaults to HEAD; OUT_DIR must not exist)

Reads committed blobs at REV (not the working tree), so the extract is tied to one commit. Writes nothing into this
repository. Publishing the extract is a separate step that needs Lawrence's word.

What goes in (found by walking the folder at REV, filtered by these prefixes): runs/ except our copy of Jang-woo's
files (his own gist is the public copy), packet/ (v1), packet-v2/, CHANGES.md, READINESS.md, and publish/ except
this script and build_publish.py (which names what it removes). Left out: review/ (internal drafts and chat links).

What is changed, and nothing else (each rule counted per file in SANITIZED.json):
  scratch   the per-session temporary folder (under AppData, Local, Temp, claude: two ids) -> <temp>
  win_user  the Windows user folder name in C:\\Users\\<name> -> <user>
  wsl_user  the WSL home folder name in /home/<name> -> <user>
  tailnet   an address inside our own tailnet block (the case-4b fixture that v2.3 replaced and treated as a
            disclosure) -> <withheld tailnet address>; 100.64.0.0 (the range itself) is kept
  surname   the operator's surname, once, in packet v1's README -> removed
The run records are otherwise byte-for-byte: a changed file's sha256 differs from the private original, and
SANITIZED.json gives both the original's git blob hash and the copy's sha256, with the counts.
"""
import hashlib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      check=True).stdout.strip()
BASE = "reviews/signed-run-packet-2026-11-17/"
INCLUDE = ("runs/", "packet/", "packet-v2/", "CHANGES.md", "READINESS.md", "publish/")
EXCLUDE = ("runs/2026-11-18-jangwoo-v2.3-gist/", "publish/build_publish.py", "publish/build_records_extract.py")
SEP = r"(?:\\+|/)"  # any run of backslashes (JSON escapes paths once, a string inside a string twice) or a slash
RULES = [
    ("scratch", re.compile(r"AppData" + SEP + r"Local" + SEP + r"Temp" + SEP + r"claude" + SEP + r"[0-9a-f]{8,}" + SEP
                           + r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"), "<temp>"),
    ("win_user", re.compile(r"(?i)([A-Z]:" + SEP + r"Users" + SEP + r")<user>\b"), r"\1<user>"),
    ("wsl_user", re.compile(r"/home/<user>\b"), "/home/<user>"),
    ("tailnet", re.compile(r"\b100\.64\.0\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9])\b"), "<withheld tailnet address>"),
    ("surname", re.compile(r"Lawrence <surname>'s"), "Lawrence's"),
]
# After the rules, none of these may remain anywhere in the extract.
LEFT = [re.compile(p) for p in (r"(?i)\b<user>\b", r"(?i)<surname>", r"(?i)Temp" + SEP + r"claude" + SEP,
                                r"\b100\.64\.0\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|[1-9])\b",
                                r"chatgpt\.com/c/|chat\.deepseek\.com/a/|claude\.ai/chat/|gemini\.google\.com/app/[0-9a-f]",
                                r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)[A-Za-z0-9.-]+\.(?:com|net|org|local)\b")]


README = """# Signed-RUN packet: our run records (cleaned copy)

The raw records behind the signed-RUN reproduction packet's `RUNS_SUMMARY.md`: the internal runs in our record of
packet v1 to v2.4, and the outsider-route runs from the published gist. The packet itself is
https://gist.github.com/LAWLESS1987/79d125f515a2a90556acbde557ae9c57; its README says these records were kept in
the Mutual Benefit Collective's private repository. This is a copy of them, made so that anyone can check our
summaries against what the runs printed.

**These are our own runs (internal preparation), not outside reproductions.** Outside runs are linked from the
packet's README and belong to the people who ran them.

Made by Claude (an AI) at Lawrence's direction, by `build_records_extract.py` (included here; see below), from
the collective's commit `%(commit)s`, folder `reviews/signed-run-packet-2026-11-17/`. That repository is
private, so the commit id cannot be checked from outside; it is given so that the copy can be traced back to it.

## What is here

%(files)s files, laid out as in the private record: `runs/` (one folder per run: `environment.json`,
`results.json`, `summary.txt`, `workers_raw.json`, and the console output), `packet/` (v1) and `packet-v2/` (v2.4,
as published), `CHANGES.md` (every version and why it changed), `READINESS.md`, and `publish/` (the files published
beside the packet). `CHANGES.md` and `READINESS.md` mention files that are not here: our internal review drafts
(`review/`), `publish/build_publish.py` (which names what it removes), and our copy of Jang-woo's return (his own
gist is the public copy).

## What was changed

Only what identifies the operator's machine or private network, and one name. Of the %(files)s record files,
%(unchanged)s are byte-for-byte the originals; in the other %(changed)s, exactly these replacements were made (counts
summed over those files):

| what | replaced by | count |
|---|---|---|
| the per-session temporary folder (under `AppData`, `Local`, `Temp`, `claude`: two ids) | `<temp>` | %(scratch)s |
| the Windows user folder name (`C:\\Users\\<name>`) | `<user>` | %(win_user)s |
| the WSL home folder name (`/home/<name>`) | `<user>` | %(wsl_user)s |
| an address inside our own tailnet's block: the case-4b fixture address of v2.0 to v2.2, replaced in v2.3 because it sat there | `<withheld tailnet address>` | %(tailnet)s |
| the operator's surname, in packet v1's README | removed | %(surname)s |

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
"""


def git(*a, binary=False):
    r = subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    out, rev = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "HEAD")
    if os.path.exists(out):
        raise SystemExit("OUT_DIR exists; refusing to overwrite: " + out)
    commit = git("rev-parse", rev).strip()
    entries = []
    for line in git("ls-tree", "-r", commit, "--", BASE).splitlines():
        meta, path = line.split("\t", 1)
        rel = path[len(BASE):]
        if rel.startswith(INCLUDE) and not rel.startswith(EXCLUDE):
            entries.append((rel, meta.split()[2]))
    manifest, problems = [], []
    for rel, blob in sorted(entries):
        data = git("cat-file", "blob", blob, binary=True)
        if b"\0" in data:
            raise SystemExit("binary file in the set, not handled: " + rel)
        text = data.decode("utf-8")
        counts = {}
        for name, rx, rep in RULES:
            text, n = rx.subn(rep, text)
            if n:
                counts[name] = n
        for rx in LEFT:
            for m in rx.finditer(text):
                problems.append("%s: %r" % (rel, text[max(0, m.start() - 20):m.end() + 5]))
        new = text.encode("utf-8")
        dst = os.path.join(out, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(new)
        manifest.append({"path": rel, "original_git_blob": blob, "sha256": hashlib.sha256(new).hexdigest(),
                         "unchanged": not counts, "replaced": counts})
    if problems:
        raise SystemExit("left in the extract (%d): %s" % (len(problems), problems[:5]))
    summary = {
        "about": "Cleaned extract of the Mutual Benefit Collective's private record for the signed-RUN packet "
                 "(issue #21). Each file is the committed original with only the replacements named in 'rules'; "
                 "'original_git_blob' is the private original's git blob hash, 'sha256' this copy's.",
        "source_commit": commit, "source_folder": BASE, "rules": {n: rep for n, _, rep in RULES},
        "files": len(manifest), "unchanged_files": sum(1 for m in manifest if m["unchanged"]),
        "replacements": {n: sum(m["replaced"].get(n, 0) for m in manifest) for n, _, _ in RULES},
        "manifest": manifest}
    with open(os.path.join(out, "SANITIZED.json"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    r = summary["replacements"]
    with open(os.path.join(out, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(README % dict(commit=commit, files=len(manifest), unchanged=summary["unchanged_files"],
                               changed=len(manifest) - summary["unchanged_files"], **r))
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    src = re.sub(r"(?i)<surname>", "<surname>", re.sub(r"(?i)<user>(?!nce)", "<user>", src))
    for rx in LEFT:
        if rx.search(src):
            raise SystemExit("redacted script copy still matches " + rx.pattern)
    with open(os.path.join(out, "build_records_extract.py"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)
    print("source", commit[:12], "| files", len(manifest), "| unchanged", summary["unchanged_files"],
          "| replacements", summary["replacements"])


if __name__ == "__main__":
    main()
