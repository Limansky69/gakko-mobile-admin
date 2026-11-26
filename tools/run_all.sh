#!/bin/bash
# usage: bash run_all.sh /ścieżka/work.html   – cała regresja po kolei, na końcu każdego scenariusza "errors: []"
D=$(cd "$(dirname "$0")" && pwd)
for f in e1 nfb cfm md rv2 z1b del more au au4 au6; do
  echo "== $f"; timeout 150 python3 -I "$D/flowx.py" "$1" "$D/flows/$f.json" 2>&1 | grep -E "errors:|CLICK FAIL|JSERR|Traceback"
done
