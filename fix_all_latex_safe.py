import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# Replace any single backslash followed by a letter with a double backslash followed by that letter.
# This safely fixes \times, \frac, \beta, etc., without affecting \" or \' or \\.
new_text = re.sub(r'(?<!\\)\\([a-zA-Z])', r'\\\\\1', text)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Backslashes safely doubled!")
