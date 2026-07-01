import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()
cats = re.findall(r'category:\s*"([^"]+)"', text)
from collections import Counter
print(Counter(cats))
