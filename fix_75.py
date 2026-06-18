import codecs

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Just search for \sqrt{ラスパイレス...} or similar
start = data.find('ラスパイレス')
if start != -1:
    print('Found ラスパイレス at', start)
    
# Let's replace the 4th option directly for ID 75
import re
def repl_75(m):
    text = m.group(0)
    text = re.sub(r'\\\\sqrt\{[^\}]*\}', r'\\\\frac{\\\\sum p_0 q_0}{\\\\sum p_t q_t} \\\\times 100', text)
    return text

data = re.sub(r'\{\s*id:\s*75.*?answerOptions:\s*\[.*?\].*?\}', repl_75, data, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(data)
print("Fixed 75.")
