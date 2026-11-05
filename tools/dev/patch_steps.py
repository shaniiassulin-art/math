# replace steps / warn / check of sections in a units file:  python3 patch_steps.py <units file> <new-steps file>
# the new-steps file defines NEW[(unit n, section id)] = (steps source, warn or None, check or None)
import re, sys, runpy
path, newf = sys.argv[1], sys.argv[2]
NEW = runpy.run_path(newf)['NEW']
s = open(path, encoding='utf-8').read()
def span(n):
    units = [m.start() for m in re.finditer(r'^dict\(\n  n=(\d+)', s, re.M)]
    nums = [int(m.group(1)) for m in re.finditer(r'^dict\(\n  n=(\d+)', s, re.M)]
    i = nums.index(n); a = units[i]; b = units[i + 1] if i + 1 < len(units) else len(s); return a, b
for (n, sid), (steps, warn, check) in sorted(NEW.items(), key=lambda kv: (kv[0][0], -int(kv[0][1][1:]))):
    ua, ub = span(n)
    m = re.compile(r"    dict\(id='%s'," % sid).search(s, ua, ub)
    assert m, (n, sid)
    a = m.start()
    nxt = re.compile(r"\n    dict\(id='|\n   \]\),").search(s, a + 10)
    e = nxt.start()
    sec = s[a:e]
    i = sec.index('      steps=[')
    j = sec.index('\n      ],', i) + len('\n      ],')
    sec = sec[:i] + '      steps=' + steps.strip() + ',' + sec[j:]
    if warn:
        sec = re.sub(r"      warn=r'.*?',\n", lambda _: "      warn=r'" + warn + "',\n", sec, count=1, flags=re.S)
    if check:
        sec = re.sub(r"      check=r'.*?'\)", lambda _: "      check=r'" + check + "')", sec, count=1, flags=re.S)
    s = s[:a] + sec + s[e:]
open(path, 'w', encoding='utf-8').write(s)
compile(s, path, 'exec')
print('patched', len(NEW))
