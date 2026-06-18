import codecs
import re
data = codecs.open('data.js', 'r', 'utf-8').read()
m = re.search(r'category:\s*"([^"]+)"[^}]*相関', data)
print('Category for correlation:', m.group(1) if m else 'Not found')
