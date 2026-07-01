import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# IDs to delete
ids_to_delete = {210, 92, 83}

blocks = re.split(r'(?=\{\s*id:\s*)', text)
new_blocks = [blocks[0]]

for b in blocks[1:]:
    id_m = re.search(r'id:\s*(\d+)', b)
    if not id_m:
        new_blocks.append(b)
        continue
    qid = int(id_m.group(1))
    
    if qid in ids_to_delete:
        # Skip this block to delete it
        continue
        
    new_blocks.append(b)

new_text = ''.join(new_blocks)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print(f"Deleted IDs: {ids_to_delete}")
