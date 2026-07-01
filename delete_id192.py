import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# We need to remove the whole object for id: 192
# Assuming it's inside the QUIZ_DATA array like:
#   {
#     id: 192,
#     ...
#   },
# Or at the end without comma.
# A regex to match the block: \s*\{\s*id:\s*192,.*?\}\s*(,|(?=\]))
new_text = re.sub(r'\s*\{\s*id:\s*192,.*?\}(?:,)?(?=\s*(?:\{|\]))', '', text, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("ID 192 deleted.")
