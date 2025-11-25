import re
from pathlib import Path

css_path = Path('static/css/style_index.css')
backup_path = css_path.with_suffix('.css.bak')
text = css_path.read_text(encoding='utf-8')
# Backup
backup_path.write_text(text, encoding='utf-8')

# Match simple selector blocks without nested braces
pattern = re.compile(r'([^{]+\{[^{}]*\})', re.S)
seen = set()
removed = 0

new_text = text
for m in pattern.finditer(text):
    block = m.group(1)
    block_norm = '\n'.join(line.strip() for line in block.splitlines() if line.strip())
    if block_norm in seen:
        # remove this exact block (match the exact substring)
        new_text = new_text.replace(block, '')
        removed += 1
    else:
        seen.add(block_norm)

if removed > 0:
    css_path.write_text(new_text, encoding='utf-8')

print(f'BACKUP: {backup_path}\nREMOVED_DUPLICATES: {removed}')
