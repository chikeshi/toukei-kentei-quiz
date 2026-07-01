import codecs
import re

old_text = codecs.open('old_data.js', 'r', 'utf-16').read()
old_blocks = old_text.split('\n  {\n    id: ')
old_cat_map = {}
for b in old_blocks[1:]:
    id_match = re.search(r'^(\d+),', b)
    cat_match = re.search(r'category:\s*"([^"]+)"', b)
    if id_match and cat_match:
        old_cat_map[int(id_match.group(1))] = cat_match.group(1)
        
print("Length of old_cat_map:", len(old_cat_map))
print(list(old_cat_map.items())[:5])
