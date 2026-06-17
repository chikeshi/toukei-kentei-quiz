import re
import codecs

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

math_exprs = re.findall(r'\$(.*?)\$', data)
math_with_slash = [m for m in math_exprs if '/' in m]
for m in sorted(list(set(math_with_slash))):
    print(m)
