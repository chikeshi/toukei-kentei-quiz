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
    m = re.search(r'id:\s*(\d+)', obj_str)
    if not m: continue
    obj_id = int(m.group(1))
    
    new_obj_str = obj_str
    
    if obj_id == 214:
        new_obj_str = """{
    id: 214,
    isFormula: 1,
    category: "確率",
    question: "確率密度関数 $f(x)$ を持ち、期待値が $\\\\mu$ である連続型確率変数 $X$ の「分散 $V[X]$」を求める定義式はどれですか？",
    answerOptions: [
      { text: "$\\\\int_{-\\\\infty}^{\\\\infty} (x - \\\\mu)^2 f(x) dx$", rationale: "分散は「平均からの偏差の2乗」の期待値として定義されます。", isCorrect: true },
      { text: "$\\\\int_{-\\\\infty}^{\\\\infty} x f(x) dx$", rationale: "これは期待値の定義式です。", isCorrect: false },
      { text: "$\\\\int_{-\\\\infty}^{\\\\infty} (x - \\\\mu) f(x) dx$", rationale: "これは平均からの偏差の期待値であり、計算すると必ず0になります。", isCorrect: false },
      { text: "$\\\\int_{-\\\\infty}^{\\\\infty} x^2 f(x) dx$", rationale: "これは $X^2$ の期待値 $E[X^2]$ であり、ここから $\\\\mu^2$ を引けば分散になります。", isCorrect: false }
    ]
  }"""

    if obj_id == 208:
        new_obj_str = """{
    id: 208,
    isFormula: 0,
    category: "確率分布",
    question: "確率変数 $X$ が「標準正規分布」に従う場合、その期待値と分散の正しい組み合わせはどれですか？",
    answerOptions: [
      { text: "期待値: $0$, 分散: $1$", rationale: "標準正規分布は、平均 $\\\\mu=0$、分散 $\\\\sigma^2=1$ に標準化された正規分布です。", isCorrect: true },
      { text: "期待値: $1$, 分散: $1$", rationale: "標準化された正規分布の期待値（平均）は $0$ です。", isCorrect: false },
      { text: "期待値: $0$, 分散: $0$", rationale: "分散が $0$ の場合、すべてのデータが $0$ になり分布を持ちません。", isCorrect: false },
      { text: "期待値: $0$, 分散: $\\\\sigma^2$", rationale: "分散は $1$ に標準化されている必要があります。", isCorrect: false }
    ]
  }"""

    if obj_id == 125:
        new_obj_str = """{
    id: 125,
    isFormula: 1,
    category: "推測統計",
    question: "母分散 $\\\\sigma^2$ が既知である正規母集団から抽出したサイズ $n$ の標本（標本平均 $\\\\bar{x}$）を用いた、「母平均 $\\\\mu$ の $95\\\\%$ 信頼区間」の公式はどれですか？（$Z_{0.025} = 1.96$ とする）",
    answerOptions: [
      { text: "$\\\\bar{x} \\\\pm 1.96 \\\\frac{\\\\sigma}{\\\\sqrt{n}}$", rationale: "母分散が既知なので標準正規分布を用い、標準誤差は $\\\\frac{\\\\sigma}{\\\\sqrt{n}}$ となります。", isCorrect: true },
      { text: "$\\\\bar{x} \\\\pm 1.96 \\\\frac{\\\\sigma^2}{n}$", rationale: "標準誤差は分散ではなく標準偏差で表します。", isCorrect: false },
      { text: "$\\\\bar{x} \\\\pm 1.64 \\\\frac{\\\\sigma}{\\\\sqrt{n}}$", rationale: "$1.64$ は $90\\\\%$ 信頼区間（$Z_{0.05}$）の係数です。$95\\\\%$ の場合は $1.96$ を用います。", isCorrect: false },
      { text: "$\\\\bar{x} \\\\pm 1.96 \\\\frac{\\\\sigma}{n}$", rationale: "分母に平方根（ルート）が抜けています。", isCorrect: false }
    ]
  }"""

    if obj_id == 171:
        new_obj_str = """{
    id: 171,
    isFormula: 1,
    category: "線形モデル",
    question: "単回帰分析 $y = \\\\hat{\\\\beta}_0 + \\\\hat{\\\\beta}_1 x$ において、切片 $\\\\hat{\\\\beta}_0$ を求める公式として正しいものはどれですか？（ただし、$S_{xy}$ は共分散または偏差積和、$S_{xx}$ は $x$ の分散または偏差平方和を表す）",
    answerOptions: [
      { text: "$\\\\hat{\\\\beta}_0 = \\\\bar{y} - \\\\frac{S_{xy}}{S_{xx}} \\\\bar{x}$", rationale: "回帰係数（傾き）は $\\\\frac{S_{xy}}{S_{xx}}$ で求められます。回帰直線は必ず平均点 $(\\\\bar{x}, \\\\bar{y})$ を通るため、$\\\\bar{y} = \\\\hat{\\\\beta}_0 + \\\\frac{S_{xy}}{S_{xx}} \\\\bar{x}$ を変形して切片を求めます。", isCorrect: true },
      { text: "$\\\\hat{\\\\beta}_0 = \\\\bar{y} + \\\\frac{S_{xy}}{S_{xx}} \\\\bar{x}$", rationale: "引き算ではなく足し算になっており誤りです。", isCorrect: false },
      { text: "$\\\\hat{\\\\beta}_0 = \\\\bar{x} - \\\\frac{S_{xy}}{S_{xx}} \\\\bar{y}$", rationale: "$x$ の平均と $y$ の平均が逆になっています。", isCorrect: false },
      { text: "$\\\\hat{\\\\beta}_0 = \\\\frac{S_{xy}}{S_{xx}}$", rationale: "これは切片 $\\\\hat{\\\\beta}_0$ ではなく、傾き $\\\\hat{\\\\beta}_1$ を求める公式です。", isCorrect: false }
    ]
  }"""

    if new_obj_str != obj_str:
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Applied strict replacements for 214, 208, 125, 171.")
