import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Parse objects
objects = []
idx = data.find('const QUIZ_DATA = [') + len('const QUIZ_DATA = [')
while True:
    start = data.find('{', idx)
    if start == -1: break
    depth = 0
    in_string = False
    escape = False
    end = -1
    str_char = ''
    for i in range(start, len(data)):
        c = data[i]
        if not in_string:
            if c == '{': depth += 1
            elif c == '}': 
                depth -= 1
                if depth == 0:
                    end = i
                    break
            elif c in ('"', "'", '`'):
                in_string = True
                str_char = c
        else:
            if escape: escape = False
            elif c == '\\': escape = True
            elif c == str_char: in_string = False
            
    if end != -1:
        obj_str = data[start:end+1]
        objects.append((start, end, obj_str))
        idx = end + 1
    else:
        break

new_data = data
for start, end, obj_str in reversed(objects):
    new_obj_str = obj_str
    
    m = re.search(r'id:\s*(\d+)', obj_str)
    if not m: continue
    obj_id = int(m.group(1))
    
    if obj_id == 78:
        new_obj_str = re.sub(r'isFormula:\s*1', 'isFormula: 0', new_obj_str)

    if new_obj_str != obj_str:
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Batch 4 modifications done.")
