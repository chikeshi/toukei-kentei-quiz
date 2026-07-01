import codecs
import re
import json

text = codecs.open('data.js', 'r', 'utf-8').read()

# Try to parse the QUIZ_DATA array
match = re.search(r'const\s+QUIZ_DATA\s*=\s*(\[.*?\]);', text, re.DOTALL)
if not match:
    # Maybe no semicolon?
    match = re.search(r'const\s+QUIZ_DATA\s*=\s*(\[.*\])', text, re.DOTALL)

if match:
    array_str = match.group(1)
    
    # We will use a JS parser in python via regex? No, just find missing commas.
    # We can check if every `}` that is followed by `{` has a comma between them!
    
    # Check for `} {` or `}\n\s*{` with no comma
    # Exclude matches that are inside strings.
    # Actually, let's just strip all strings first, then look for `} {`
    
    no_strings = re.sub(r'"([^"\\]|\\.)*"', '""', array_str)
    no_strings = re.sub(r"'([^'\\]|\\.)*'", "''", no_strings)
    
    missing_commas = re.findall(r'\}\s*\{', no_strings)
    if missing_commas:
        print("FOUND MISSING COMMAS BETWEEN BRACES:", len(missing_commas))
        
    missing_commas_array = re.findall(r'\]\s*\{', no_strings)
    if missing_commas_array:
        print("FOUND MISSING COMMAS BETWEEN ARRAY AND BRACE:", len(missing_commas_array))

    print("Check 1 complete.")
    
    # Check for double commas
    double_commas = re.findall(r',\s*,', no_strings)
    if double_commas:
        print("FOUND DOUBLE COMMAS:", len(double_commas))

