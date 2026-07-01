import re
text = r'\times \beta \\gamma'
print("Original:", repr(text))
new_text = re.sub(r'(?<!\\)\\([a-zA-Z])', r'\\\\\1', text)
print("Replaced:", repr(new_text))
