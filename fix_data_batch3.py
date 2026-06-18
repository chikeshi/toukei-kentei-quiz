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

ids_to_delete = [135, 217, 174, 65, 121, 207, 162]
ids_to_unformula = [191, 61, 45, 41, 60, 222]

new_data = data
for start, end, obj_str in reversed(objects):
    new_obj_str = obj_str
    
    m = re.search(r'id:\s*(\d+)', obj_str)
    if not m: continue
    obj_id = int(m.group(1))
    
    # 1. Delete
    if obj_id in ids_to_delete:
        comma_idx = data.find(',', end+1)
        if comma_idx != -1 and data[end+1:comma_idx].strip() == '':
            new_data = new_data[:start] + new_data[comma_idx+1:]
        else:
            new_data = new_data[:start] + new_data[end+1:]
        continue
    
    # 2. isFormula to 0
    if obj_id in ids_to_unformula:
        new_obj_str = re.sub(r'isFormula:\s*1', 'isFormula: 0', new_obj_str)
        
    # 3. Modify ID 68
    if obj_id == 68:
        new_obj_str = new_obj_str.replace(
            r'text: "\\bar{x} \\pm 1.64 \\frac{\\sigma}{\\sqrt{n}}"',
            r'text: "\\bar{x} \\pm 1.96 \\frac{\\sigma}{\\sqrt{n-1}}"'
        )
        new_obj_str = re.sub(
            r'rationale:\s*"[^"]*1\.64[^"]*"',
            r'rationale: "分母が $n-1$ になっており誤りです。"',
            new_obj_str
        )

    # 4. Modify ID 167
    elif obj_id == 167:
        new_obj_str = new_obj_str.replace(
            r'text: "$t = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}"',
            r'text: "$Z = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}"'
        )
        new_obj_str = re.sub(
            r'rationale:\s*"[^"]*t検定の検定量です[^"]*"',
            r'rationale: "母分散既知なので、標本標準偏差 $s$ は使いません。"',
            new_obj_str
        )
        new_obj_str = new_obj_str.replace(
            r'text: "$\\chi^2 = \\frac{(n-1)s^2}{\\sigma^2}"',
            r'text: "$Z = \\frac{\\bar{x} - \\mu_0}{\\sigma^2 / n}"'
        )
        new_obj_str = re.sub(
            r'rationale:\s*"[^"]*カイ二乗検定の検定量です[^"]*"',
            r'rationale: "分母が分散になっており誤りです。"',
            new_obj_str
        )

    if new_obj_str != obj_str:
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Batch 3 modifications done.")
