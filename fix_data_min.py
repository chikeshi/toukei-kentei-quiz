import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# 1. Terminology adjustments globally
data = data.replace('群間平方和(水準間平方和)', '群間平方和')
data = data.replace('群内平方和(残差平方和)', '群内平方和')
data = data.replace('群間平方和', '群間平方和(水準間平方和)')
data = data.replace('群内平方和', '群内平方和(残差平方和)')
data = data.replace('郡内平方和', '群内平方和(残差平方和)')

# Delete IDs
ids_to_delete = [200, 169, 209, 88, 185, 99]

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
    
    if obj_id in ids_to_delete:
        comma_idx = data.find(',', end+1)
        if comma_idx != -1 and data[end+1:comma_idx].strip() == '':
            new_data = new_data[:start] + new_data[comma_idx+1:]
        else:
            new_data = new_data[:start] + new_data[end+1:]
        continue
        
    if obj_id == 218:
        new_obj_str = new_obj_str.replace(r'text: "\\frac{\\bar{x}_1 - \\bar{x}_2}{SE}"', r'text: "\\frac{\\bar{d}}{s_d^2 / n}"')
        new_obj_str = new_obj_str.replace(r'text: "\\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}"', r'text: "\\frac{\\bar{d}}{s_d / n}"')
        new_obj_str = new_obj_str.replace(r'text: "\\frac{\\sum(O-E)^2}{E}"', r'text: "\\frac{\\bar{d}}{\\sqrt{s_d / n}}"')

    elif obj_id == 216:
        new_obj_str = new_obj_str.replace(r'text: "\\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}}"', r'text: "\\frac{\\bar{x} - \\mu_0}{s^2 / \\sqrt{n}}"')
        new_obj_str = new_obj_str.replace(r'text: "\\frac{\\bar{d}}{s_d / \\sqrt{n}}"', r'text: "\\frac{\\bar{x} - \\mu_0}{s / n}"')
        new_obj_str = new_obj_str.replace(r'text: "\\frac{\\bar{x}_1 - \\bar{x}_2}{SE}"', r'text: "\\frac{\\bar{x} - \\mu_0}{\\sqrt{s} / n}"')

    elif obj_id == 163:
        # Match using regex for the text field
        new_obj_str = re.sub(r'text:\s*"[^"]*（※?\$X\$ と \$Y\$ が独立な場合に限る）"', r'text: "$E(aX + bY) = a^2 E(X) + b^2 E(Y)$"', new_obj_str)

    elif obj_id == 71:
        new_obj_str = new_obj_str.replace(r'text: "\\hat{p} \\pm 1.64 \\sqrt{\\frac{p(1-p)}{n}}"', r'text: "\\hat{p} \\pm 1.96 \\sqrt{\\frac{p}{n}}"')

    elif obj_id == 212:
        new_obj_str = re.sub(r'text:\s*"[^"]*Cov\[X,Y\][^"]*"', r'text: "$E[XY] + E[X]E[Y]$"', new_obj_str)

    elif obj_id == 75:
        new_obj_str = re.sub(r'text:\s*"[^"]*ラスパイレス指数 \\times パーシェ指数[^"]*"', r'text: "\\frac{\\sum p_0 q_0}{\\sum p_t q_t} \\times 100"', new_obj_str)

    if new_obj_str != obj_str:
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Minimal replacements done.")
