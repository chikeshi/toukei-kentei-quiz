import codecs
import re
import json

def extract_questions(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as f:
        data = f.read()

    match = re.search(r'const\s+QUIZ_DATA\s*=\s*\[', data)
    if not match:
        return []
    
    start_idx = match.end()
    brace_depth = 0
    in_string = False
    escape_next = False
    block_start = -1
    
    questions = []
    
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
                    q_match = re.search(r'["\']?question["\']?\s*:\s*["\'](.*?)["\']\s*,', block_text, re.DOTALL)
                    opts_match = re.findall(r'text\s*:\s*["\'](.*?)["\']', block_text)
                    
                    if id_match and q_match:
                        q_id = int(id_match.group(1))
                        # Only include if it has exactly 4 options (meaning it hasn't been processed yet)
                        if len(opts_match) == 4:
                            questions.append({
                                'id': q_id,
                                'question': q_match.group(1).replace('\\n', ' ').strip()
                            })
                    block_start = -1
            elif char == ']':
                if brace_depth == 0:
                    break
        i += 1
        
    return questions

qs = extract_questions('data.js')
with codecs.open('questions_dump.json', 'w', 'utf-8') as f:
    json.dump(qs, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(qs)} questions with 4 options.")
