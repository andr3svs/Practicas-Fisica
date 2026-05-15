from pathlib import Path
import re
p = Path('m33_report.tex')
t = p.read_text(encoding='utf-8')
pat = re.compile(r'\\qty\{([^}]*)\}\{([^}]*)\}')

def repl(m):
    v = m.group(1)
    u = m.group(2)
    if u == '^\\circ C':
        return '\\ensuremath{' + v + '\\,^{\\circ}\\mathrm{C}}'
    return '\\ensuremath{' + v + '\\,\\mathrm{' + u + '}}'

count = t.count('\\qty{')
new = pat.sub(repl, t)
p.write_text(new, encoding='utf-8')
print(f'replaced {count} occurrences')
