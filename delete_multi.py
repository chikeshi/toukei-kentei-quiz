import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# Using regex to split at the start of each object
# The objects look like:
#   {
#     id: 1,
#
# We will split by a regex that looks for `{ id:` ignoring whitespace
blocks = re.split(r'\{\s*id:\s*', text)
new_blocks = [blocks[0]]

deleted_ids = []

for b in blocks[1:]:
    # Each block 'b' starts with the ID number followed by a comma
    match = re.match(r'^(\d+),', b)
    if match:
        q_id = int(match.group(1))
        if q_id in [70, 218, 192]:
            print(f"Skipping ID {q_id}")
            deleted_ids.append(q_id)
            # We need to remove the trailing comma from the PREVIOUS block if this was the last block, 
            # but usually they are followed by other blocks, except the very last one.
            # We'll handle this cleanly by re-joining.
            
            # Note: b ends with "  }, \r\n  " or "  }\r\n];"
            # If we skip it, we might end up with double commas if we just rejoin?
            # Wait, re.split removed `{ id: `. It left `},\r\n  ` at the end of the previous block?
            # No, `b` contains the rest of the object AND the comma AND whitespace until the next `{ id: `.
            # If we just skip 'b', we lose the closing `}` of the deleted object, but also we lose the comma separating it from the NEXT object!
            # Which is PERFECT! Because if we skip an element, the previous element's trailing stuff connects to `{ id:` of the NEXT element.
            # Wait, let's trace:
            # text = "A {id: 1} , B {id: 2} , C {id: 3} D"
            # split('{id: '): ["A ", "1} , B ", "2} , C ", "3} D"]
            # skip 2: ["A ", "1} , B ", "3} D"]
            # join('{id: '): "A {id: 1} , B {id: 3} D"
            # This is PERFECT!
            continue
    new_blocks.append(b)

new_text = '{ id: '.join(new_blocks)

# Fix any potential double commas like "  }, \n  , " or similar just in case
# The above logic should be perfectly clean.
# Let's fix the formatting of '{ id: ' to match the original style:
new_text = new_text.replace('{ id: ', '{\n    id: ')

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Deleted IDs:", deleted_ids)
