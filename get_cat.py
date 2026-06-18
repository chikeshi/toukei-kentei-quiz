import codecs
import re
data = codecs.open('data.js', 'r', 'utf-8').read()
cats = set(re.findall(r'category:\s*"([^"]+)"', data))
with codecs.open('cats.txt', 'w', 'utf-8') as f:
    for c in cats:
        f.write(c + '\n')
