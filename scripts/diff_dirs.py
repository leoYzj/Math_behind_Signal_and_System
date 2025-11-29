from pathlib import Path
from difflib import unified_diff

oldp = Path('d:/code_clone/Math_behind_Signal_and_System/Math_behind_Signal_and_System.tex')
newp = Path(str(oldp) + '.joined.tex')
old = oldp.read_text(encoding='utf-8').splitlines()
new = newp.read_text(encoding='utf-8').splitlines()

print('Total old lines:', len(old))
print('Total new lines:', len(new))

diff = list(unified_diff(old, new, fromfile=str(oldp), tofile=str(newp), lineterm=''))
print('Total diff lines:', len(diff))

# Print some sample chunks
printed = 0
for line in diff:
    if printed > 300:
        break
    print(line)
    printed += 1
