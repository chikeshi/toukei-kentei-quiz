import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Fix missing commas between objects
new_data = re.sub(r'\}\s*\{', '}, {', data)

# Fix any double commas just in case
new_data = re.sub(r',\s*,', ',', new_data)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Fixed syntax errors.")
