import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# 1. Delete ID 117
# We can just split by ID blocks and exclude ID 117
blocks = re.split(r'(?=\{\s*id:\s*)', text)
new_blocks = [blocks[0]]

for b in blocks[1:]:
    id_m = re.search(r'id:\s*(\d+)', b)
    if not id_m:
        new_blocks.append(b)
        continue
    qid = int(id_m.group(1))
    
    if qid == 117:
        # Skip this block to delete it
        continue
        
    # 2. Fix 4 backslashes in ID 213 and 214
    if qid in [213, 214]:
        # The broken options have 4 backslashes for \int, \infty, \mu
        # e.g., \\\\int -> \\int
        # We can just replace '\\\\int' with '\\int' etc, but wait, 
        # inside python string literal, '\\\\\\\\' is 4 backslashes.
        # Let's just use string replace.
        b = b.replace(r'\\\\int', r'\\int')
        b = b.replace(r'\\\\infty', r'\\infty')
        b = b.replace(r'\\\\mu', r'\\mu')
        
    new_blocks.append(b)

new_text = ''.join(new_blocks)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Deleted ID 117 and fixed LaTeX backslashes in IDs 213, 214.")
