import codecs
import re
import json
import glob

# Load all distractors
distractors = {}
for file_name in glob.glob('distractors_*.json'):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            distractors[item['id']] = item

def inject_distractors(file_path, distractors_map):
    with codecs.open(file_path, 'r', 'utf-8') as f:
        data = f.read()

    match = re.search(r'const\s+QUIZ_DATA\s*=\s*\[', data)
    if not match:
        print("Could not find QUIZ_DATA array start")
        return
    
    start_idx = match.end()
    new_data = data[:start_idx]
    
    brace_depth = 0
    in_string = False
    escape_next = False
    block_start = -1
    
    blocks = []
    
    i = start_idx
    while i < len(data):
        char = data[i]
        
        if escape_next:
            escape_next = False
            i += 1
            continue
            
        if char == '\\':
            escape_next = True
            i += 1
            continue
            
        if char == '"' or char == "'":
            if not in_string:
                in_string = char
            elif in_string == char:
                in_string = False
            i += 1
            continue
            
        if not in_string:
            if char == '{':
                if brace_depth == 0:
                    block_start = i
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
                if brace_depth == 0 and block_start != -1:
                    block_text = data[block_start:i+1]
                    
                    id_match = re.search(r'["\']?id["\']?\s*:\s*(\d+)', block_text)
                    if id_match:
                        q_id = int(id_match.group(1))
                        
                        if q_id in distractors_map:
                            dist = distractors_map[q_id]
                            # Count current options
                            opts_match = re.findall(r'text\s*:\s*["\'].*?["\']', block_text)
                            if len(opts_match) == 4:
                                # We need to inject the 5th option at the end of answerOptions array
                                # Find 'answerOptions': [ ... ]
                                opts_start = re.search(r'["\']?answerOptions["\']?\s*:\s*\[', block_text)
                                if opts_start:
                                    # Find matching bracket for answerOptions
                                    o_start = opts_start.end()
                                    o_depth = 1
                                    o_end = -1
                                    o_in_string = False
                                    o_esc = False
                                    
                                    for j in range(o_start, len(block_text)):
                                        c = block_text[j]
                                        if o_esc:
                                            o_esc = False
                                            continue
                                        if c == '\\':
                                            o_esc = True
                                            continue
                                        if c == '"' or c == "'":
                                            if not o_in_string:
                                                o_in_string = c
                                            elif o_in_string == c:
                                                o_in_string = False
                                            continue
                                        if not o_in_string:
                                            if c == '[': o_depth += 1
                                            elif c == ']':
                                                o_depth -= 1
                                                if o_depth == 0:
                                                    o_end = j
                                                    break
                                    
                                    if o_end != -1:
                                        # Construct new option string
                                        escaped_text = dist['text'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                                        escaped_rationale = dist['rationale'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                                        new_opt_str = f',      {{ text: "{escaped_text}", rationale: "{escaped_rationale}", isCorrect: false }}\n    '
                                        
                                        # Inject it
                                        block_text = block_text[:o_end] + new_opt_str + block_text[o_end:]
                                        print(f"Injected 5th option for ID: {q_id}")
                    
                    blocks.append(block_text)
                    block_start = -1
            elif char == ']':
                if brace_depth == 0:
                    break
        i += 1
                    
    array_end_idx = data.find(']', i)
    new_data += '\n  ' + ',\n  '.join(blocks) + '\n' + data[array_end_idx:]
    
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(new_data)
        
inject_distractors('data.js', distractors)
