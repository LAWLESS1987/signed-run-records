# Reviewer return: signed-RUN packet v2.4

Fill in what you're comfortable sharing. Leave anything blank, or write "not shared". Nothing here is required.

**Before you attach output:** `summary.txt`, `results.json`, `workers_raw.json` and `environment.json` contain your
local paths (the temporary folder, your clone, the Python executable, the current folder). You may replace any of them
with `<redacted>`. Please say which files you edited and how, so we can tell your edits from the tool's output.

## Who ran it
- Name or handle, as you'd like it shown (or "anonymous"):
- Did you read the packet before running it? (all / part / no):
- Did you read the covenant lines listed in README section 1? (all / part / no):

## What you ran
- Covenant source: clone or zip? If a clone, the output of `git -C <clone> rev-parse ead187b2513fba7bce1404cf3678ae128f38b1b8`:
- sha256 of `run_packet.py` and `expected.json` as you ran them (printed on the third line, and in `environment.json`):
- How you got the packet (link):
- The exact commands, including setup (clone or download, venv, pip install):

## Where you ran it
- OS and version:
- Machine kind (bare metal / VM / container / WSL / other):
- Was the network disconnected during the run? (yes / no / don't know):
- Python version:
- flask, werkzeug, cryptography versions (in `environment.json`):
- git version, if used:

## What happened
- Exit code:
- The RESULT line, copied:
- Run time (on the RESULT line):
- Every line marked `DIFF` or `inconclusive`, with its variant:
- Any `NOTE` lines (network events, unexpected modules, outside writes):
- Raw output: `summary.txt`, or the console output. Also `results.json` and `workers_raw.json`, if you're willing.

## Differences
- Anything you had to change to make it run (code, command, environment), exactly:
- Any help you needed from us, and what it was:
- Anything that came out differently from `expected.json` or from our runs in `RUNS_SUMMARY.md`:
- Anything in README or CLAIM.md that you think is wrong, unclear, or claims more than the run shows:

## Your judgement (optional)
- Does the packet test what CLAIM.md says it tests? Where does it fall short?
- A case or a break you think is missing:

## Publishing
- May we publish this return beside our own runs, unedited apart from your redactions? (yes / yes, without my name / no):
