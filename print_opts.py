import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()
ids = ['66', '68', '72', '96', '118', '175', '198', '225']

for qid in ids:
    m = re.search(r'\{\s*id:\s*' + qid + r',.*?\n  \}', text, re.DOTALL)
    if m:
        opts = re.findall(r'text:\s*"(.*?)"', m.group(0))
        print(f'ID {qid}:')
        for o in opts:
            print(f'  {o}')
