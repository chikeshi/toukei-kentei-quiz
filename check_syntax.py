import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()
blocks = text.split('\n  {\n    id: ')

for i, b in enumerate(blocks[1:]):
    b = "{\n    id: " + b
    if i == len(blocks[1:]) - 1:
        b = b[:b.rfind(';')] # remove trailing ;
        if b.endswith(']'): b = b[:-1] # remove trailing ]
        b = b.strip()
    
    if b.count('{') != b.count('}'):
        print(f"Mismatch braces in block {i+1}: {b.count('{')} != {b.count('}')}")
    if b.count('[') != b.count(']'):
        print(f"Mismatch brackets in block {i+1}: {b.count('[')} != {b.count(']')}")
        
print("Check complete.")
