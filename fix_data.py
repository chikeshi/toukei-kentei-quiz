import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# 1. Delete IDs 188, 131, 133
ids_to_delete = [188, 131, 133]
for i in ids_to_delete:
    pattern = r'\s*\{\s*id:\s*' + str(i) + r'.*?answerOptions:\s*\[.*?\].*?\},?'
    data = re.sub(pattern, '', data, flags=re.DOTALL)

# 2. Modify ID 198
def repl_198(m):
    text = m.group(0)
    text = text.replace("群間平方和 S_A", "水準間平方和 S_A")
    text = text.replace("群内平方和 S_E", "残差平方和 S_E")
    text = text.replace("群数 a", "水準の数 a")
    text = text.replace("群間の", "水準間の")
    text = text.replace("群内の", "残差の")
    return text

data = re.sub(r'\{\s*id:\s*198.*?answerOptions:\s*\[.*?\].*?\}', repl_198, data, flags=re.DOTALL)

# 3. Modify ID 127
new_formula = r"$F_{1-\alpha/2}(n_1-1, n_2-1) \times \frac{s_2^2}{s_1^2} \le \frac{\sigma_2^2}{\sigma_1^2} \le F_{\alpha/2}(n_1-1, n_2-1) \times \frac{s_2^2}{s_1^2}$"
# In data.js, a JS string must have double backslashes to result in a single backslash for KaTeX.
new_formula_js = new_formula.replace('\\', '\\\\')

def repl_127(m):
    text = m.group(0)
    # Use re.sub with lambda to avoid escape processing in the replacement string
    return re.sub(
        r'text:\s*"\$\\\\left\[ \\\\frac\{s_1\^2\}\{s_2\^2\} \\\\frac\{1\}\{F_U\}, \\\\frac\{s_1\^2\}\{s_2\^2\} \\\\frac\{1\}\{F_L\} \\\\right\]\$"',
        lambda _: 'text: "' + new_formula_js + '"',
        text
    )

data = re.sub(r'\{\s*id:\s*127.*?answerOptions:\s*\[.*?\].*?\}', repl_127, data, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(data)

print("Modifications done.")
