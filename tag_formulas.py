import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

def is_formula_question(q_text, options_text):
    keywords = ["式", "関数", "統計量", "推定量", "導出", "計算"]
    for kw in keywords:
        if kw in q_text:
            return True
            
    math_count = 0
    for opt in options_text:
        stripped = opt.strip()
        if stripped.startswith('$') and stripped.endswith('$'):
            math_count += 1
            
    if math_count >= 2:
        return True
        
    return False

# Since the file format is very regular, we can split by `{ id: `
parts = data.split('{ id: ')

new_parts = [parts[0]]

for part in parts[1:]:
    # Find the end of the question object. It usually ends with `} },` or `} }`
    # Let's just find `question: "..."`
    q_match = re.search(r'question:\s*"(.*?)"\s*,\s*answerOptions:', part, re.DOTALL)
    if q_match:
        q_text = q_match.group(1)
        
        opts_texts = re.findall(r'text:\s*"(.*?)"\s*,\s*rationale:', part, re.DOTALL)
        
        formula_flag = is_formula_question(q_text, opts_texts)
        flag_val = 1 if formula_flag else 0
        
        # prepend `isFormula: X, ` to the part
        # wait, the part already starts with `123, category: ...`
        
        # let's just insert it after the id. The part starts with something like `1, category:`
        # We can regex match the `\d+,` at the start.
        part = re.sub(r'^(\d+\s*,)', r'\1 isFormula: ' + str(flag_val) + ',', part)
        
    new_parts.append(part)

new_data = '{ id: '.join(new_parts)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Tagging done.")
