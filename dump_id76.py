import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

m = re.search(r'\{\s*id:\s*76\b.*?\s*answerOptions:\s*\[.*?\]\s*\}', data, re.DOTALL)
if m:
    with codecs.open('id76.txt', 'w', 'utf-8') as f:
        f.write(m.group(0))
    print("Exported ID 76")
else:
    print("ID 76 not found")
