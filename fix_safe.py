import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Custom object extractor
def find_objects(data_str):
    objects = []
    idx = data_str.find('const QUIZ_DATA = [') + len('const QUIZ_DATA = [')
    while True:
        start = data_str.find('{', idx)
        if start == -1: break
        depth = 0
        in_string = False
        escape = False
        str_char = ''
        end = -1
        for i in range(start, len(data_str)):
            c = data_str[i]
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
            objects.append((start, end, data_str[start:end+1]))
            idx = end + 1
        else:
            break
    return objects

objects = find_objects(data)
new_data = data

# Iterate backwards so replacements don't shift indices of earlier items
for start, end, obj_str in reversed(objects):
    m = re.search(r'id:\s*(\d+)', obj_str)
    if not m: continue
    obj_id = int(m.group(1))
    
    if obj_id in [215, 86, 128, 173]:
        # Delete object
        new_data = new_data[:start] + "" + new_data[end+1:]
        continue
        
    if obj_id == 214:
        # replace the discrete formula with the continuous expectation of deviation
        new_obj_str = re.sub(r'\{\s*text:\s*".*?\\sum_\{x\}.*?",\s*rationale:\s*".*?",\s*isCorrect:\s*false\s*\}',
                             '{ text: "\\\\int_{-\\\\infty}^{\\\\infty} (x - \\\\mu) f(x) dx", rationale: "これは平均からの偏差の期待値であり、計算すると必ず0になります。", isCorrect: false }', obj_str)
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

    elif obj_id == 208:
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
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

    elif obj_id == 125:
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
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

    elif obj_id == 171:
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
        new_data = new_data[:start] + new_obj_str + new_data[end+1:]

# Add IDs 230, 231
new_qs = """  , {
    id: 230,
    isFormula: 0,
    category: "推測統計",
    question: "実験計画法における「フィッシャーの3原則（局所管理、反復、無作為化）」のそれぞれを行使することによる実験への影響や目的の記述として、最も不適切な（間違っている）ものはどれですか。",
    answerOptions: [
      { text: "「反復」とは、実験全体を1回だけ行い、その中で多様な条件を試すことで、測定誤差を完全に排除する原則である。", rationale: "反復（繰り返し）は、同じ条件下で実験を複数回行うことで誤差の大きさを評価し、精度を高めるための原則であり、1回だけの実験や誤差の完全な排除を意味しません。", isCorrect: true },
      { text: "「無作為化（ランダム化）」とは、実験順序や配置をくじ引きなどの偶然に任せて決定することで、制御できない未知の要因による系統的な偏りを相殺する原則である。", rationale: "正しい記述です。未知の要因を偶然誤差に転化し、偏り（バイアス）を防ぎます。", isCorrect: false },
      { text: "「局所管理」とは、実験を行う空間や時間を細かいブロックに区切り、ブロック内での条件をできるだけ均一に保つことで、環境による系統的な誤差を小さくする原則である。", rationale: "正しい記述です。ブロック化により系統誤差を分離・排除し、実験の精度を向上させます。", isCorrect: false },
      { text: "無作為化と局所管理は系統誤差（偏り）に対処するための原則であり、反復は偶然誤差（ばらつき）を評価するための原則である。", rationale: "正しい記述です。それぞれの原則の役割を正確に説明しています。", isCorrect: false }
    ]
  }, {
    id: 231,
    isFormula: 0,
    category: "時系列・指数",
    question: "時系列データの変化や推移を捉えるための4つの指標［差、比、変化率（伸び率）、指数］の計算式や特徴に関する記述として、最も適切なものはどれですか。",
    answerOptions: [
      { text: "「指数」は、ある特定の時点（基準時）の値を $100$ として、他の時点（比較時）の値がどの程度の割合になるかを算出したものであり、単位の異なるデータ間の推移を比較するのに適している。", rationale: "指数の定義として正確であり、単位に依存せず長期的な推移や複数系列の比較に用いられます。", isCorrect: true },
      { text: "「変化率（伸び率）」は、比較時の値から基準時の値を引いた「差」として定義され、パーセント（$\\\\%$）ではなく元のデータと同じ単位で表される。", rationale: "誤りです。変化率（伸び率）は「（比較時 - 基準時）/ 基準時」で計算され、通常は $\\\\%$ で表されます。説明文は「差」の特徴です。", isCorrect: false },
      { text: "「比」は、前年の値から当年の値を引くことによって求められ、系列全体の絶対的な増減量を把握するために用いられる。", rationale: "誤りです。比は「当年 / 前年」のように割り算で求めます。引き算で求めるのは「差」です。", isCorrect: false },
      { text: "「差」は、異なる単位を持つ2つの時系列データ（例：金額と重量）の変化の度合いを直接比較するのに最も適した指標である。", rationale: "誤りです。「差」は元のデータと同じ単位を持つため、単位の異なるデータの比較には適しません。単位の異なる比較には「変化率」や「指数」を用います。", isCorrect: false }
    ]
  }"""

idx = new_data.rfind(']')
if idx != -1:
    new_data = new_data[:idx] + new_qs + '\n' + new_data[idx:]

# Clean up any missing or extra commas
# Replace `} {` or `}\n\s*{` with `}, {`
new_data = re.sub(r'\}\s*\{', '}, {', new_data)
# Replace `, ,` with `,`
new_data = re.sub(r',\s*,', ',', new_data)
# Replace `[ ,` with `[`
new_data = re.sub(r'\[\s*,', '[', new_data)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Safe modifications applied.")
