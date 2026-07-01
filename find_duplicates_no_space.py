import codecs
import re
from collections import Counter

text = codecs.open('data.js', 'r', 'utf-8').read()
blocks = re.split(r'(?=\{\s*id:\s*)', text)[1:]

for b in blocks:
    id_m = re.search(r'id:\s*(\d+)', b)
    if not id_m: continue
    qid = id_m.group(1)
    
    opts = re.findall(r'text:\s*"(.*?)"', b)
    # Strip spaces for comparison
    opts_no_space = [o.replace(' ', '') for o in opts]
    
    c = Counter(opts_no_space)
    dups = [k for k,v in c.items() if v > 1]
    if dups:
        print(f"ID {qid} has duplicates (ignoring spaces): {dups}")
