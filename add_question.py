import codecs

new_q = """  , {
    id: 225,
    isFormula: 1,
    category: "線形モデル",
    question: "変数 $z$ の影響を取り除いた、変数 $x, y$ 間の偏相関係数 $r_{xy \\\\cdot z}$ を求める式はどれですか？",
    answerOptions: [
      { text: "$\\\\frac{r_{xy} - r_{xz} r_{yz}}{\\\\sqrt{1 - r_{xz}^2} \\\\sqrt{1 - r_{yz}^2}}$", rationale: "偏相関係数の正しい定義式です。$z$ の影響を除外するために計算されます。", isCorrect: true },
      { text: "$\\\\frac{r_{xy} - r_{xz} r_{yz}}{\\\\sqrt{1 - r_{xy}^2} \\\\sqrt{1 - r_{yz}^2}}$", rationale: "分母の $r_{xz}^2$ が $r_{xy}^2$ になっており誤りです。", isCorrect: false },
      { text: "$\\\\frac{r_{xy} - r_{xz} r_{yz}}{\\\\sqrt{1 - r_{xz}^2} + \\\\sqrt{1 - r_{yz}^2}}$", rationale: "分母が掛け算ではなく足し算になっており誤りです。", isCorrect: false },
      { text: "$\\\\frac{r_{xy} - r_{xz} r_{yz}}{1 - r_{xz} r_{yz}}$", rationale: "分母の形がまったく異なり誤りです。", isCorrect: false }
    ]
  }"""

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# find the last closing brace of the array
idx = data.rfind(']')
if idx != -1:
    new_data = data[:idx] + new_q + '\n' + data[idx:]
    with codecs.open('data.js', 'w', 'utf-8') as f:
        f.write(new_data)
    print("Added new question successfully.")
else:
    print("Could not find the end of the array.")
