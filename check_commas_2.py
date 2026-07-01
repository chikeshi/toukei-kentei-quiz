import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()
no_strings = re.sub(r'"([^"\\]|\\.)*"', '""', text)
no_strings = re.sub(r"'([^'\\]|\\.)*'", "''", no_strings)

matches = list(re.finditer(r'\}\s*\{', no_strings))
for m in matches[:10]:
    print("Match at:", m.start())
    print("Original text context:")
    print(repr(text[m.start()-20:m.end()+20]))
    
