import codecs
import re
import json

with open('fixed_distractors.json', 'r', encoding='utf-8') as f:
    fixes = json.load(f)
    
fix_map = {item['id']: item for item in fixes}

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

match = re.search(r'const\s+QUIZ_DATA\s*=\s*\[', data)
start_idx = match.end()

brace_depth = 0
in_string = False
escape_next = False
block_start = -1

blocks = []

i = start_idx
while i < len(data):
    char = data[i]
    if escape_next:
        escape_next = False; i += 1; continue
    if char == '\\':
        escape_next = True; i += 1; continue
    if char == '"' or char == "'":
        if not in_string: in_string = char
        elif in_string == char: in_string = False
        i += 1; continue
        
    if not in_string:
        if char == '{':
            if brace_depth == 0: block_start = i
            brace_depth += 1
        elif char == '}':
            brace_depth -= 1
            if brace_depth == 0 and block_start != -1:
                block_text = data[block_start:i+1]
                id_match = re.search(r'["\']?id["\']?\s*:\s*(\d+)', block_text)
                
                if id_match:
                    q_id = int(id_match.group(1))
                    if q_id in fix_map:
                        new_opt = fix_map[q_id]
                        
                        array_start = block_text.rfind('[')
                        array_end = block_text.rfind(']')
                        
                        if array_start != -1 and array_end != -1:
                            array_content = block_text[array_start:array_end]
                            opts_start = array_content.rfind('{')
                            opts_end = array_content.rfind('}')
                            
                            if opts_start != -1 and opts_end != -1:
                                escaped_text = new_opt['text'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                                escaped_rationale = new_opt['rationale'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                                
                                replacement = f'{{ text: "{escaped_text}", rationale: "{escaped_rationale}", isCorrect: false }}'
                                new_array_content = array_content[:opts_start] + replacement + array_content[opts_end+1:]
                                
                                block_text = block_text[:array_start] + new_array_content + block_text[array_end:]
                                print(f"Fixed ID: {q_id}")
                
                blocks.append(block_text)
                block_start = -1
        elif char == ']':
            if brace_depth == 0: break
    i += 1
    
new_data = data[:start_idx] + '\n  ' + ',\n  '.join(blocks) + '\n' + data[data.find(']', i):]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)
