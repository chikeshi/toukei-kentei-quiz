import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

blocks = re.split(r'(?=\{\s*id:\s*)', text)
new_blocks = [blocks[0]]

prefixes_to_remove = [
    'Z = ', 'Z=',
    't = ', 't=',
    'F = ', 'F=',
    '\\\\chi^2 = ', '\\\\chi^2='
]

for b in blocks[1:]:
    q_match = re.search(r'question:\s*"(.*?)"', b)
    if not q_match:
        new_blocks.append(b)
        continue
        
    question_text = q_match.group(1)
    
    # Check if question specifies the test statistic
    # "統計量 Z は", "統計量 t は", "F は", "\chi^2", "カイ二乗"
    has_Z = bool(re.search(r'\bZ\b', question_text))
    has_t = bool(re.search(r'\bt\b', question_text))
    has_F = bool(re.search(r'\bF\b', question_text))
    has_chi2 = bool(re.search(r'chi\^2|χ|カイ二乗|カイ2乗', question_text))
    
    # If the question specifies a test statistic, we remove prefixes.
    if has_Z or has_t or has_F or has_chi2:
        lines = b.split('\n')
        new_lines = []
        for line in lines:
            if 'text: "$' in line:
                for prefix in prefixes_to_remove:
                    target = f'text: "${prefix}'
                    if target in line:
                        line = line.replace(target, 'text: "$')
            new_lines.append(line)
        b = '\n'.join(new_lines)
    
    new_blocks.append(b)

new_text = ''.join(new_blocks)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Smart prefix removal complete.")
