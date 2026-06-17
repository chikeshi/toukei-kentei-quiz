import re
import codecs

try:
    with codecs.open('data.js', 'r', encoding='utf-8') as f:
        data = f.read()
    print("UTF-8 success")
except Exception as e:
    print("UTF-8 fail:", e)
    with codecs.open('data.js', 'r', encoding='shift_jis') as f:
        data = f.read()
    print("SJIS fallback")

cats = re.findall(r'category:\s*[\"\']([^\"\']+)[\"\']', data)
from collections import Counter
print(Counter(cats))
