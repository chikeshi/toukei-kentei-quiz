import codecs

text = codecs.open('data.js', 'r', 'utf-8').read()

new_question = """  ,{
    id: 235,
    isFormula: 1,
    category: "仮説検定",
    question: "2つの独立な標本（サイズ $n_1, n_2$、標本比率 $\\\\hat{p}_1, \\\\hat{p}_2$）を用いて「母比率の差の検定」を行う際、帰無仮説 $p_1 = p_2$ のもとで用いる「プールされた比率（共通比率）$\\\\hat{p}$」の定義式はどれですか？",
    answerOptions: [
      { text: "$\\\\frac{n_1\\\\hat{p}_1 + n_2\\\\hat{p}_2}{n_1 + n_2}$", rationale: "2つの標本を合わせた全体の「成功回数（$n_1\\\\hat{p}_1 + n_2\\\\hat{p}_2$）」を、全体の「標本サイズの和（$n_1 + n_2$）」で割ったものがプールされた比率です。", isCorrect: true },
      { text: "$\\\\frac{\\\\hat{p}_1 + \\\\hat{p}_2}{2}$", rationale: "単純な相加平均ではありません。2つの標本サイズ（$n_1$ と $n_2$）が異なる場合に結果が歪んでしまいます。", isCorrect: false },
      { text: "$\\\\sqrt{\\\\hat{p}_1 \\\\hat{p}_2}$", rationale: "相乗平均ではありません。", isCorrect: false },
      { text: "$\\\\frac{n_1\\\\hat{p}_1 - n_2\\\\hat{p}_2}{n_1 + n_2}$", rationale: "分子は差（マイナス）ではなく、合わせた成功回数の和（プラス）になります。", isCorrect: false },
      { text: "$\\\\frac{\\\\hat{p}_1(1-\\\\hat{p}_1)}{n_1} + \\\\frac{\\\\hat{p}_2(1-\\\\hat{p}_2)}{n_2}$", rationale: "これは「母比率の差の信頼区間」を求める際に用いられる、比率の差の分散の推定量です。", isCorrect: false }
    ]
  }\n];"""

text_before = text.rsplit('];', 1)[0]
if not text_before.endswith('\n'):
    text_before += '\n'

new_text = text_before + new_question

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Added pooled proportion question.")
