from pathlib import Path

root = Path(__file__).resolve().parents[1]
for path in [*root.glob('*.html'), *root.glob('*.json'), *root.glob('*.txt'), *root.glob('*.py')]:
    if path.name == 'case_fix.py':
        continue
    text = path.read_text(encoding='utf-8')
    updated = text.replace('AILENS', 'AiLens').replace('AILens', 'AiLens')
    if updated != text:
        path.write_text(updated, encoding='utf-8')
print('Normalized visible brand capitalization to AiLens; domain URLs remain unchanged.')
