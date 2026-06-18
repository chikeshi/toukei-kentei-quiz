import codecs
import re
data = codecs.open('data.js', 'r', 'utf-8').read()
m = re.search(r'category:\s*"([^"]+)"[^}]*相関', data)
with codecs.open('cat_cor.txt', 'w', 'utf-8') as f:
    f.write(m.group(1) if m else 'Not found')
