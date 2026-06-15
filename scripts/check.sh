#!/usr/bin/env bash
# check.sh — validation harness for the FiezDev profile README.
# Encodes the doc-pack acceptance criteria (T1 structure → T3 content → T4 QA).
# Usage: bash scripts/check.sh    (run from repo root)
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
README="$ROOT/README.md"
FAIL=0
pass() { printf '  \033[32m✓\033[0m %s\n' "$1"; }
fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; FAIL=1; }

echo "── Structure ────────────────────────────"
[ -f "$README" ] && pass "README.md exists" || { fail "README.md missing"; echo; echo "FAILED"; exit 1; }
[ -d "$ROOT/assets" ] && pass "assets/ dir exists" || fail "assets/ dir missing"

# line number of first regex match (empty = not found)
lineof() { grep -nE -m1 -- "$1" "$README" 2>/dev/null | cut -d: -f1; }

B=$(lineof '<img[^>]*assets/banner\.svg')   # the actual banner <img>, not the header comment
W=$(lineof '^#{1,3} .*Selected Work')        # real heading only
T=$(lineof '^#{1,3} .*Tech Stack')
C=$(lineof '^#{1,3} .*Connect')

[ -n "$B" ] && pass "banner reference present (line $B)" || fail "banner (assets/banner.svg) reference missing"
[ -n "$W" ] && pass "Selected Work section present (line $W)" || fail "Selected Work section missing"
[ -n "$T" ] && pass "Tech Stack section present (line $T)" || fail "Tech Stack section missing"
[ -n "$C" ] && pass "Connect section present (line $C)" || fail "Connect section missing"

echo "── Section order (banner → Work → Stack → Connect) ──"
if [ -n "$B" ] && [ -n "$W" ] && [ -n "$T" ] && [ -n "$C" ]; then
  if [ "$B" -lt "$W" ] && [ "$W" -lt "$T" ] && [ "$T" -lt "$C" ]; then
    pass "sections appear in the correct order"
  else
    fail "sections out of order (banner=$B work=$W stack=$T connect=$C)"
  fi
else
  fail "cannot verify order — a section is missing"
fi

echo "── Privacy / honesty guards (forbidden content) ──"
# Only the 4 approved contacts; no phone/LINE/CodePen/Facebook; no seniority title.
guard() { if grep -qiE -- "$1" "$README" 2>/dev/null; then fail "forbidden: $2"; else pass "absent: $2"; fi; }
guard '\+?66 ?9 ?1 ?7 ?2 ?1 ?0 ?2 ?7 ?4|0917210274'  "phone number"
guard 'line\.me|gdrx1135'                              "LINE contact"
guard 'codepen'                                        "CodePen link"
guard 'facebook\.com|qoneainews'                       "Facebook link"
guard '\bSenior\b|\blead engineer\b'                   "seniority/position title"

echo "── Approved contacts present (skeleton may not have them yet) ──"
soft() { if grep -qiE -- "$1" "$README" 2>/dev/null; then pass "present: $2"; else printf '  \033[33m•\033[0m %s (not yet — ok pre-content)\n' "$2"; fi; }
soft 'itti\.task@gmail\.com'      "email"
soft 'linkedin\.com/in/fiezdev'   "LinkedIn"
soft 'fiez\.dev'                  "portfolio link"
soft 'github\.com/FiezDev'        "GitHub link"

echo
if [ "$FAIL" -eq 0 ]; then printf '\033[32mALL CHECKS PASSED\033[0m\n'; else printf '\033[31mCHECKS FAILED\033[0m\n'; fi
exit $FAIL
