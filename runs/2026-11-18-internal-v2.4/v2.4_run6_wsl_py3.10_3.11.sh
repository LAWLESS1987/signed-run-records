#!/bin/bash
# Full packet v2.4 (all cases, incl. 10_planted_json) under uv Python 3.10.21 and 3.11.16, WSL.
# Packet files: the published LF bytes (CRLF stripped from ~/v24/pkt, then checked against the published sha256).
# Venvs + pip install happen first, with network; the run itself under unshare -rn + env -i, as Jang-woo ran v2.3.
set -u
B=~/v24py
mkdir -p $B/pkt
tr -d '\r' < ~/v24/pkt/run_packet.py > $B/pkt/run_packet.py
tr -d '\r' < ~/v24/pkt/expected.json > $B/pkt/expected.json
echo "run_packet.py sha256 $(sha256sum < $B/pkt/run_packet.py | cut -c1-64)  (published 380e91f204b7fb01886b6936652e7eec35031bc40c931c47d2dc85c796c9ea62)"
echo "expected.json git blob $(git hash-object --no-filters $B/pkt/expected.json)  (published 4fdb71c207ead8e785fd2723b5ce8a7b00357608)"
echo "run_packet.py git blob $(git hash-object --no-filters $B/pkt/run_packet.py)  (published c008b5203d1ca852e152b7dd3a9b76bfc4f3862b)"
mkdir -p $B/home_empty
for v in 3.10.21 3.11.16; do
  V=$B/venv-$v
  if [ ! -x $V/bin/python ]; then
    ~/.local/bin/uv venv --python $v $V >/dev/null 2>&1 || { echo "venv $v FAILED"; continue; }
    ~/.local/bin/uv pip install --python $V/bin/python flask cryptography 2>&1 | tail -3
  fi
  echo "=== $v: $($V/bin/python -c 'import sys,flask,cryptography,importlib.metadata as m;print(sys.version.split()[0],"flask",m.version("flask"),"werkzeug",m.version("werkzeug"),"cryptography",cryptography.__version__)')"
  rm -rf $B/out_$v
  cd $B/pkt
  if unshare -rn true 2>/dev/null; then WRAP="unshare -rn"; else WRAP=""; echo "(unshare -rn unavailable; network NOT cut)"; fi
  echo "wrapper: ${WRAP:-none}"
  $WRAP env -i PATH=/usr/bin:/bin HOME=$B/home_empty LANG=C.UTF-8 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
    $V/bin/python run_packet.py --covenant ~/v24/cov --out $B/out_$v > $B/run_$v.console.txt 2>&1
  echo "exit $?"
  grep -n "^python\|10_planted\|RESULT\|DIFF\|NOTE\|inconclusive" $B/run_$v.console.txt
done
