import codecs
import re

def delete_ids(file_path, ids_to_delete):
    with codecs.open(file_path, 'r', 'utf-8') as f:
        data = f.read()

    # Find where the array starts
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
            # Very basic string handling, assuming no unescaped quotes
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
                    # block complete
                    block_text = data[block_start:i+1]
                    
                    # Extract ID (allow optional quotes)
                    id_match = re.search(r'["\']?id["\']?\s*:\s*(\d+)', block_text)
                    if id_match:
                        block_id = int(id_match.group(1))
                        if block_id not in ids_to_delete:
                            blocks.append(block_text)
                        else:
                            print(f"Deleted ID: {block_id}")
                    else:
                        blocks.append(block_text)
                    block_start = -1
            elif char == ']':
                if brace_depth == 0:
                    # End of array
                    break
        i += 1
                    
    # Reconstruct the array
    array_end_idx = data.find(']', i)
    
    new_data += '\n  ' + ',\n  '.join(blocks) + '\n' + data[array_end_idx:]
    
    with codecs.open(file_path, 'w', 'utf-8') as f:
        f.write(new_data)
        
ids = [75, 115, 119, 178, 134, 184]
delete_ids('data.js', ids)
