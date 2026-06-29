import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

def find_objects(data_str):
    objects = []
    idx = data_str.find('const QUIZ_DATA = [') + len('const QUIZ_DATA = [')
    while True:
        start = data_str.find('{', idx)
        if start == -1: break
        depth = 0
        in_string = False
        escape = False
        str_char = ''
        end = -1
        for i in range(start, len(data_str)):
            c = data_str[i]
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
            objects.append(data_str[start:end+1])
            idx = end + 1
        else:
            break
    return objects

objects = find_objects(data)
ids_to_check = ['12', '29', '43', '77', '78', '79', '80', '127', '198', '222']

for obj_str in objects:
    m = re.search(r'id:\s*(\d+)', obj_str)
    if m and m.group(1) in ids_to_check:
        cat_match = re.search(r'category:\s*"(.*?)"', obj_str)
        q_match = re.search(r'question:\s*"(.*?)"', obj_str)
        print(f"ID {m.group(1)}: [{cat_match.group(1) if cat_match else 'None'}] {q_match.group(1)[:50] if q_match else 'None'}...")
