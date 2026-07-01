import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# Delete ID 73
blocks = re.split(r'(?=\{\s*id:\s*)', text)
new_blocks = [blocks[0]]

for b in blocks[1:]:
    id_m = re.search(r'id:\s*(\d+)', b)
    if not id_m:
        new_blocks.append(b)
        continue
    qid = int(id_m.group(1))
    
    if qid == 73:
        # Skip this block to delete it
        continue
        
    new_blocks.append(b)

new_text = ''.join(new_blocks)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Deleted ID 73.")
