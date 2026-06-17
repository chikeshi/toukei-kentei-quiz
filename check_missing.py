import json
import re

content = open('quiz.js', encoding='utf-8').read()
m = re.search(r'const QUIZ_DATA = (\[.*?\]);', content, re.DOTALL)
if not m:
    print("Not found")
    exit()

data_str = m.group(1).replace('false', 'False').replace('true', 'True')
data = eval(data_str)

missing = 0
total = 0
for q in data:
    for a in q['answerOptions']:
        total += 1
        if 'rationale' not in a:
            missing += 1

print(f"Missing rationales: {missing} / {total}")
