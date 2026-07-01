import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

blocks = text.split('\n  {\n    id: ')
new_blocks = [blocks[0]]

for b in blocks[1:]:
    id_match = re.search(r'^(\d+),', b)
    if id_match and int(id_match.group(1)) == 192:
        print("Skipping ID 192")
        continue
    new_blocks.append(b)

new_text = '\n  {\n    id: '.join(new_blocks)

# We need to make sure the last block's trailing comma is handled if 192 was the last block, 
# but 192 is not the last block (max ID is >200). 
# Wait, if 192 was the last block, the trailing array closing `];` would be part of the last block anyway.

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("ID 192 successfully removed.")
