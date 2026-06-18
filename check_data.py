import codecs
import re
data = codecs.open('data.js', 'r', 'utf-8').read()
ids=[int(x) for x in re.findall(r'id:\s*(\d+)', data)]
print('Max ID:', max(ids) if ids else 0)
cats=set(re.findall(r'category:\s*"([^"]+)"', data))
for c in cats: print(c)
