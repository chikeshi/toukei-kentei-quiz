import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# 1. Terminology adjustments globally
data = data.replace('群間平方和(水準間平方和)', '群間平方和')
data = data.replace('群内平方和(残差平方和)', '群内平方和')
data = data.replace('群間平方和', '群間平方和(水準間平方和)')
data = data.replace('群内平方和', '群内平方和(残差平方和)')
data = data.replace('郡内平方和', '群内平方和(残差平方和)')

# 2. Extract objects using a robust brace matcher
objects = []
idx = data.find('const QUIZ_DATA = [') + len('const QUIZ_DATA = [')

while True:
    start = data.find('{', idx)
    if start == -1: break
    
    depth = 0
    in_string = False
    escape = False
    end = -1
    str_char = ''
    
    for i in range(start, len(data)):
        c = data[i]
        if not in_string:
            if c == '{': depth += 1
            elif c == '}': 
                depth -= 1
                if depth == 0:
                    end = i
                    break
            elif c in ('"', "'", '`'):
                in_string = True
                str_char = c
        else:
            if escape: escape = False
            elif c == '\\': escape = True
            elif c == str_char: in_string = False
            
    if end != -1:
        obj_str = data[start:end+1]
        objects.append((start, end, obj_str))
        idx = end + 1
    else:
        break

ids_to_delete = [200, 169, 209, 88, 185, 99]

new_data = data
for start, end, obj_str in reversed(objects):
    new_obj_str = obj_str
    
    m = re.search(r'id:\s*(\d+)', obj_str)
    if not m: continue
    obj_id = int(m.group(1))
    
    if obj_id in ids_to_delete:
        comma_idx = data.find(',', end+1)
        if comma_idx != -1 and data[end+1:comma_idx].strip() == '':
            new_data = new_data[:start] + new_data[comma_idx+1:]
        else:
            new_data = new_data[:start] + new_data[end+1:]
        continue
        
    if obj_id == 218:
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{\\bar{x}_1 - \\bar{x}_2}{SE}", rationale: "は対応のない「2標本の母平均の差」の検定量です。", isCorrect: false}',
            r'{text: "\\frac{\\bar{d}}{s_d^2 / n}", rationale: "分母が分散になっており誤りです。", isCorrect: false}'
        )
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{\\bar{x} - \\mu_0}{s / \\sqrt{n}}", rationale: "は1標本t検定の検定量です。", isCorrect: false}',
            r'{text: "\\frac{\\bar{d}}{s_d / n}", rationale: "分母がルートになっておらず誤りです。", isCorrect: false}'
        )
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{\\sum(O-E)^2}{E}", rationale: "は $\\chi^2$ の検定量です。", isCorrect: false}',
            r'{text: "\\frac{\\bar{d}}{\\sqrt{s_d / n}}", rationale: "分母のルートの中に分散があるが、形が異なるため誤りです。", isCorrect: false}'
        )

    elif obj_id == 216:
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{\\bar{x} - \\mu_0}{\\sigma / \\sqrt{n}}", rationale: "は母分散既知の場合の z 統計量です。", isCorrect: false}',
            r'{text: "\\frac{\\bar{x} - \\mu_0}{s^2 / \\sqrt{n}}", rationale: "分母が分散になっており誤りです。", isCorrect: false}'
        )
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{\\bar{d}}{s_d / \\sqrt{n}}", rationale: "は「対応のあるt検定」で用いる検定量です。", isCorrect: false}',
            r'{text: "\\frac{\\bar{x} - \\mu_0}{s / n}", rationale: "分母がルートになっておらず誤りです。", isCorrect: false}'
        )
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{\\bar{x}_1 - \\bar{x}_2}{SE}", rationale: "は「2標本t検定」で用いる検定量です。", isCorrect: false}',
            r'{text: "\\frac{\\bar{x} - \\mu_0}{\\sqrt{s} / n}", rationale: "分母がルートsになっており誤りです。", isCorrect: false}'
        )

    elif obj_id == 163:
        new_obj_str = new_obj_str.replace(
            r'{text: "$E(aX + bY) = aE(X) + bE(Y)$ （※ $X$ と $Y$ が独立な場合に限る）", rationale: "期待値の線形性は $X$ と $Y$ が独立「でなくても」成り立ちます。", isCorrect: false}',
            r'{text: "$E(aX + bY) = a^2 E(X) + b^2 E(Y)$", rationale: "これは分散の公式 $V(aX+bY)$ の独立な場合と混同しています。", isCorrect: false}'
        )
        # Without "※" just in case:
        new_obj_str = new_obj_str.replace(
            r'{text: "$E(aX + bY) = aE(X) + bE(Y)$ （ $X$ と $Y$ が独立な場合に限る）", rationale: "期待値の線形性は $X$ と $Y$ が独立「でなくても」成り立ちます。", isCorrect: false}',
            r'{text: "$E(aX + bY) = a^2 E(X) + b^2 E(Y)$", rationale: "これは分散の公式 $V(aX+bY)$ の独立な場合と混同しています。", isCorrect: false}'
        )

    elif obj_id == 71:
        new_obj_str = new_obj_str.replace(
            r'{text: "\\hat{p} \\pm 1.64 \\sqrt{\\frac{p(1-p)}{n}}", rationale: "$1.64$ は $90\\%$ 信頼区間の係数です。また、母比率 $p$ は $\\hat{p}$ で代用します。", isCorrect: false}',
            r'{text: "\\hat{p} \\pm 1.96 \\sqrt{\\frac{p}{n}}", rationale: "標準誤差の分子の形が誤っています。", isCorrect: false}'
        )

    elif obj_id == 212:
        new_obj_str = new_obj_str.replace(
            r'{text: "\\frac{Cov[X,Y]}{\\sqrt{V[X]V[Y]}}", rationale: "は相関係数 $\\rho$ の定義です。", isCorrect: false}',
            r'{text: "$E[XY] + E[X]E[Y]$", rationale: "マイナスがプラスになっており誤りです。", isCorrect: false}'
        )

    elif obj_id == 75:
        new_obj_str = new_obj_str.replace(
            r'{text: "\\sqrt{ラスパイレス指数 \\times パーシェ指数}", rationale: "これは「フィッシャー指数」の式です。", isCorrect: false}',
            r'{text: "\\frac{\\sum p_0 q_0}{\\sum p_t q_t} \\times 100", rationale: "基準年と比較年が逆になっており誤りです。", isCorrect: false}'
        )

    if new_obj_str != obj_str:
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Final exact modifications done.")
