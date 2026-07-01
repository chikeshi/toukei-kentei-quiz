import codecs
import re

def find_duplicates(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as f:
        data = f.read()

    match = re.search(r'const\s+QUIZ_DATA\s*=\s*\[', data)
    if not match:
        print("Could not find QUIZ_DATA")
        return
    
    start_idx = match.end()
    brace_depth = 0
    in_string = False
    escape_next = False
    block_start = -1
    
    duplicates = []
    
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
                        # Find all text fields
                        opts_match = re.findall(r'text\s*:\s*["\'](.*?)["\']', block_text)
                        
                        # Strip whitespace and compare
                        seen = set()
                        for opt in opts_match:
                            clean_opt = opt.strip()
                            if clean_opt in seen:
                                duplicates.append((q_id, clean_opt))
                                break
                            seen.add(clean_opt)
                            
                    block_start = -1
            elif char == ']':
                if brace_depth == 0:
                    break
        i += 1
        
    for q_id, opt in duplicates:
        print(f"ID {q_id} has duplicate: {opt}")
        
    print(f"Total duplicates found: {len(duplicates)}")

find_duplicates('data.js')
