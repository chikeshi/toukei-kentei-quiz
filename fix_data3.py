import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# 1. Terminology adjustments globally
# Replace carefully so we don't double replace
data = data.replace('群間平方和(水準間平方和)', '群間平方和')
data = data.replace('群内平方和(残差平方和)', '群内平方和')
data = data.replace('群間平方和', '群間平方和(水準間平方和)')
data = data.replace('群内平方和', '群内平方和(残差平方和)')
data = data.replace('郡内平方和', '群内平方和(残差平方和)')

# 2. Delete IDs
ids_to_delete = [200, 169, 209, 88, 185, 99]
for i in ids_to_delete:
    pattern = r'\s*\{\s*id:\s*' + str(i) + r'.*?answerOptions:\s*\[.*?\].*?\},?'
    data = re.sub(pattern, '', data, flags=re.DOTALL)

# 3. ID 218 fixes (d-bar everywhere)
def repl_218(m):
    text = m.group(0)
    # the text has double backslashes in the file
    text = text.replace(r'\\frac{\\bar{x}_1 - \\bar{x}_2}{SE}', r'\\frac{\\bar{d}}{s_d^2 / n}')
    text = text.replace(r'\\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}', r'\\frac{\\bar{d}}{s_d / n}')
    text = text.replace(r'\\frac{\\sum(O-E)^2}{E}', r'\\frac{\\bar{d}}{\\sqrt{s_d / n}}')
    text = text.replace('は対応のない「2標本の母平均の差」の検定量', 'は分母が分散になっており誤り')
    text = text.replace('は1標本t検定の検定量', 'は分母がルートになっておらず誤り')
    text = text.replace('は $\\chi^2$ の検定量', 'は分母がルートの中に分散があるが、形が異なるため誤り')
    return text
data = re.sub(r'\{\s*id:\s*218.*?answerOptions:\s*\[.*?\].*?\}', repl_218, data, flags=re.DOTALL)

# 4. ID 216 fixes (s everywhere)
def repl_216(m):
    text = m.group(0)
    text = text.replace(r'\\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}}', r'\\frac{\\bar{x} - \\mu_0}{s^2 / \\sqrt{n}}')
    text = text.replace(r'\\frac{\\bar{d}}{s_d / \\sqrt{n}}', r'\\frac{\\bar{x} - \\mu_0}{s / n}')
    text = text.replace(r'\\frac{\\bar{x}_1 - \\bar{x}_2}{SE}', r'\\frac{\\bar{x} - \\mu_0}{\\sqrt{s} / n}')
    text = text.replace('は母分散既知の場合の z 統計量', 'は分母が分散になっており誤り')
    text = text.replace('は「対応のあるt検定」で用いる検定量', 'は分母がルートになっておらず誤り')
    text = text.replace('は「2標本t検定」で用いる検定量', 'は分母がルートsになっており誤り')
    return text
data = re.sub(r'\{\s*id:\s*216.*?answerOptions:\s*\[.*?\].*?\}', repl_216, data, flags=re.DOTALL)

# 5. ID 163 fixes (remove text constraint)
def repl_163(m):
    text = m.group(0)
    # The string might contain literal "（※ $X$ と $Y$ が独立な場合に限る）" or just "（ $X$ と $Y$ が独立な場合に限る）"
    # Let's use regex for safer replacement
    text = re.sub(r'\$E\(aX \+ bY\) = aE\(X\) \+ bE\(Y\)\$.*?独立.*?限る.*?"', r'$E(aX + bY) = a^2 E(X) + b^2 E(Y)$"', text)
    text = text.replace('期待値の線形性は $X$ と $Y$ が独立「でなくても」成り立ちます', 'これは分散の公式 $V(aX+bY)$ の独立な場合と混同しています')
    text = text.replace('は分散の公式 $V(aX+bY)$ の独立な場合と混同しています', 'は分散の公式 $V(aX+bY)$ の独立な場合と混同しています') # just in case
    return text
data = re.sub(r'\{\s*id:\s*163.*?answerOptions:\s*\[.*?\].*?\}', repl_163, data, flags=re.DOTALL)

# 6. ID 71 fixes (1.96 everywhere)
def repl_71(m):
    text = m.group(0)
    text = text.replace(r'\\hat{p} \\pm 1.64 \\sqrt{\\frac{p(1-p)}{n}}', r'\\hat{p} \\pm 1.96 \\sqrt{\\frac{p}{n}}')
    text = text.replace(r'$1.64$ は $90\\%$ 信頼区間の係数です。また、母比率 $p$ は $\\hat{p}$ で代用します', '標準誤差の分子の形が誤っています')
    return text
data = re.sub(r'\{\s*id:\s*71.*?answerOptions:\s*\[.*?\].*?\}', repl_71, data, flags=re.DOTALL)

# 7. ID 212 fixes (remove Cov from options)
def repl_212(m):
    text = m.group(0)
    text = re.sub(r'\\\\frac\{Cov\[X,Y\]\}.*?"', r'E[XY] + E[X]E[Y]"', text)
    text = text.replace('は相関係数 $\\rho$ の定義です', 'はマイナスがプラスになっており誤りです')
    return text
data = re.sub(r'\{\s*id:\s*212.*?answerOptions:\s*\[.*?\].*?\}', repl_212, data, flags=re.DOTALL)

# 8. ID 75 fixes (remove text formula)
def repl_75(m):
    text = m.group(0)
    text = re.sub(r'\\\\sqrt\{.*?\}', r'\\frac{\\sum p_0 q_0}{\\sum p_t q_t} \\times 100', text)
    text = text.replace('これは「フィッシャー指数」の式です', '基準年と比較年が逆になっており誤りです')
    return text
data = re.sub(r'\{\s*id:\s*75.*?answerOptions:\s*\[.*?\].*?\}', repl_75, data, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(data)

print("Modifications done 2.")
