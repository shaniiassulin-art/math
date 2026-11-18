#!/usr/bin/env bash
# בנייה מחדש של שלושת אתרי הלמידה ושל דף הבית, מעמודי הבסיס (קומיט 63ea96c).
# שימוש:  bash tools/rebuild.sh   (מתוך תיקיית הריפו)
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -c 'import latex2mathml' 2>/dev/null || pip install -q --break-system-packages latex2mathml
git checkout 63ea96c -- algebra-solutions/index.html algebra-theory/index.html calculus-1/index.html
python3 tools/theory_base.py                    # טקסטים קבועים באתר התיאורטי (5 מצגות)
python3 tools/files_section.py algebra-theory   # קבצי הקורס באתר התיאורטי - המצגות החדשות
python3 tools/units.py
timeout 300 python3 tools/samples.py
timeout 300 python3 tools/samples.py
python3 build_hub.py
