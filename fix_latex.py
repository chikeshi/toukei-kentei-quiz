import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

def fix_latex(match):
    full_str = match.group(0)
    inner_text = match.group(1)
    
    # If the text contains '\' (meaning LaTeX macros) but NO '$', it's probably missing $
    if '\\' in inner_text and '$' not in inner_text:
        # Avoid things like plain text with backslashes? 
        # But this is a math quiz, if it has \frac, \lambda etc it's LaTeX.
        if re.search(r'\\[a-zA-Z]+', inner_text) or '^' in inner_text or '_' in inner_text:
            print(f"Fixing: {inner_text}")
            return full_str.replace(inner_text, f"${inner_text}$")
            
    return full_str

new_text = re.sub(r'\{\s*text:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', fix_latex, text)

# Also check for single quotes if any
new_text = re.sub(r"\{\s*text:\s*'([^'\\]*(?:\\.[^'\\]*)*)'", fix_latex, new_text)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)
