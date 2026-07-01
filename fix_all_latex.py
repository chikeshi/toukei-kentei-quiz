import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

# We need to find all strings in quotes.
# This might be tricky because of escaped quotes \", but in our file it's mostly "..."
# A safer way is to just replace single backslashes with double backslashes
# everywhere, EXCEPT where it's already double backslashes.

# Actually, the problem is that `\n` might be a literal newline sequence `\` `n` that we WANT to keep as `\n`?
# Wait! Does `data.js` contain `\n` for actual newlines?
# Let's check if there are literal `\n` intended as newlines.
# Usually data.js has actual physical newlines `\r\n`.

# Let's just double all backslashes that are not followed by another backslash,
# AND not preceded by another backslash.
# (?<!\\)\\(?!\\)

new_text = re.sub(r'(?<!\\)\\(?!\\)', r'\\\\', text)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Backslashes doubled!")
