import codecs
import re
import json

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Strip const QUIZ_DATA = 
data = re.sub(r'^.*?const\s+QUIZ_DATA\s*=\s*', '', data, flags=re.DOTALL)
# Strip trailing ;
data = re.sub(r';\s*$', '', data)

# Add quotes to keys
data = re.sub(r'([{,]\s*)([a-zA-Z0-9_]+)\s*:', r'\1"\2":', data)

try:
    json.loads(data)
    print("No JSON syntax error found!")
except json.JSONDecodeError as e:
    print(f"JSON Syntax error: {e}")
    # print context
    start = max(0, e.pos - 50)
    end = min(len(data), e.pos + 50)
    print("Context around error:")
    print(data[start:end])
