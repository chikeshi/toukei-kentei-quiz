import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Modify ID 68
def repl_68(m):
    text = m.group(0)
    # The 4th option
    text = text.replace(r'1.64 \\frac{\\sigma}{\\sqrt{n}}', r'1.96 \\frac{\\sigma}{\\sqrt{n-1}}')
    text = re.sub(r'rationale:\s*"[^"]*1\.64[^"]*"', r'rationale: "分母が $n-1$ になっており誤りです。"', text)
    return text
data = re.sub(r'\{\s*id:\s*68.*?answerOptions:\s*\[.*?\].*?\}', repl_68, data, flags=re.DOTALL)

# Modify ID 167
def repl_167(m):
    text = m.group(0)
    # The 3rd option
    text = text.replace(r'$t = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}$', r'$Z = \\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}$')
    text = re.sub(r'rationale:\s*"[^"]*t検定の検定量です[^"]*"', r'rationale: "母分散既知なので、標本標準偏差 $s$ は使いません。"', text)
    # The 4th option
    text = text.replace(r'$\\chi^2 = \\frac{(n-1)s^2}{\\sigma^2}$', r'$Z = \\frac{\\bar{x} - \\mu_0}{\\sigma^2 / n}$')
    text = re.sub(r'rationale:\s*"[^"]*カイ二乗検定の検定量です[^"]*"', r'rationale: "分母が分散になっており誤りです。"', text)
    return text
data = re.sub(r'\{\s*id:\s*167.*?answerOptions:\s*\[.*?\].*?\}', repl_167, data, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(data)

print("Minimal fixes for 68 and 167 done.")
