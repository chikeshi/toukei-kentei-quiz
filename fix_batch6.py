import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

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

new_data = data
for start, end, obj_str in reversed(objects):
    new_obj_str = obj_str
    
    m = re.search(r'id:\s*(\d+)', obj_str)
    if not m: continue
    obj_id = int(m.group(1))
    
    if obj_id in [215, 86, 128, 173]:
        new_data = new_data[:start] + "" + new_data[end+1:]
        continue
        
    if obj_id == 214:
        # replace option 3
        old_op = r'\{ text: "\\\\sum_\{x\} \(x - \\\\mu\)\^2 P\(X=x\)", rationale: "これは離散型確率変数の分散の定義式です。", isCorrect: false \}'
        new_op = '{ text: "\\\\int_{-\\\\infty}^{\\\\infty} (x - \\\\mu) f(x) dx", rationale: "これは平均からの偏差の期待値であり、計算すると必ず0になります。", isCorrect: false }'
        new_obj_str = re.sub(old_op, new_op, new_obj_str)
        
    if obj_id == 208:
        # replace options
        new_obj_str = re.sub(r'\{ text: "期待値: \\\\mu, 分散: \\\\sigma\^2".*?\}', '{ text: "期待値: $1$, 分散: $1$", rationale: "標準化された正規分布の期待値（平均）は $0$ です。", isCorrect: false }', new_obj_str, flags=re.DOTALL)
        new_obj_str = re.sub(r'\{ text: "期待値: \$1\$, 分散: \$0\$".*?\}', '{ text: "期待値: $0$, 分散: $0$", rationale: "分散が $0$ の場合、すべてのデータが $0$ になり分布を持ちません。", isCorrect: false }', new_obj_str, flags=re.DOTALL)
        new_obj_str = re.sub(r'\{ text: "期待値: \\\\frac\{1\}\{\\\\lambda\}, 分散: \\\\frac\{1\}\{\\\\lambda\^2\}".*?\}', '{ text: "期待値: $0$, 分散: $\\\\sigma^2$", rationale: "分散は $1$ に標準化されている必要があります。", isCorrect: false }', new_obj_str, flags=re.DOTALL)
        
    if obj_id == 125:
        old_op = r'\{ text: "\\\\bar\{x\} \\\\pm t_\{0\.025\}\(n-1\) \\\\frac\{\\\\sigma\}\{\\\\sqrt\{n\}\}".*?\}'
        new_op = '{ text: "\\\\bar{x} \\\\pm 1.64 \\\\frac{\\\\sigma}{\\\\sqrt{n}}", rationale: "$1.64$ は $90\\\\%$ 信頼区間（$Z_{0.05}$）の係数です。$95\\\\%$ の場合は $1.96$ を用います。", isCorrect: false }'
        new_obj_str = re.sub(old_op, new_op, new_obj_str, flags=re.DOTALL)
        
    if obj_id == 171:
        new_q = 'question: "単回帰分析 $y = \\\\hat{\\\\beta}_0 + \\\\hat{\\\\beta}_1 x$ において、切片 $\\\\hat{\\\\beta}_0$ を求める公式として正しいものはどれですか？（ただし、$S_{xy}$ は共分散または偏差積和、$S_{xx}$ は $x$ の分散または偏差平方和を表す）",'
        new_obj_str = re.sub(r'question: "単回帰分析.*?\}', new_q + '\n    answerOptions: [\n' +
            '      { text: "$\\\\hat{\\\\beta}_0 = \\\\bar{y} - \\\\frac{S_{xy}}{S_{xx}} \\\\bar{x}$", rationale: "回帰係数（傾き）は $\\\\frac{S_{xy}}{S_{xx}}$ で求められます。回帰直線は必ず平均点 $(\\\\bar{x}, \\\\bar{y})$ を通るため、$\\\\bar{y} = \\\\hat{\\\\beta}_0 + \\\\frac{S_{xy}}{S_{xx}} \\\\bar{x}$ を変形して切片を求めます。", isCorrect: true },\n' +
            '      { text: "$\\\\hat{\\\\beta}_0 = \\\\bar{y} + \\\\frac{S_{xy}}{S_{xx}} \\\\bar{x}$", rationale: "引き算ではなく足し算になっており誤りです。", isCorrect: false },\n' +
            '      { text: "$\\\\hat{\\\\beta}_0 = \\\\bar{x} - \\\\frac{S_{xy}}{S_{xx}} \\\\bar{y}$", rationale: "$x$ の平均と $y$ の平均が逆になっています。", isCorrect: false },\n' +
            '      { text: "$\\\\hat{\\\\beta}_0 = \\\\frac{S_{xy}}{S_{xx}}$", rationale: "これは切片 $\\\\hat{\\\\beta}_0$ ではなく、傾き $\\\\hat{\\\\beta}_1$ を求める公式です。", isCorrect: false }\n' +
            '    ]\n  }', new_obj_str, flags=re.DOTALL)

    if new_obj_str != obj_str:
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

new_data = re.sub(r',\s*,', ',', new_data)
new_data = re.sub(r'\[\s*,', '[', new_data)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Batch 6 modifications done.")
