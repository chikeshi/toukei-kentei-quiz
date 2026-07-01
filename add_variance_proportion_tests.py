import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

new_questions = """  ,{
    id: 232,
    isFormula: 1,
    category: "仮説検定",
    question: "正規母集団から抽出された標本に基づく「母分散の検定」で用いられる検定統計量はどれですか？（標本サイズを $n$、標本不偏分散を $s^2$、帰無仮説の母分散を $\\\\sigma_0^2$ とする）",
    answerOptions: [
      { text: "$\\\\chi^2 = \\\\frac{(n-1)s^2}{\\\\sigma_0^2}$", rationale: "母分散の検定には、不偏分散 $s^2$ を用いた $\\\\chi^2$ 統計量（自由度 $n-1$）が用いられます。", isCorrect: true },
      { text: "$\\\\chi^2 = \\\\frac{ns^2}{\\\\sigma_0^2}$", rationale: "標本サイズ $n$ をそのままかけるのは誤りです。標本分散（$n$で割ったもの）を使う場合は $n$ になりますが、不偏分散を用いる場合は $(n-1)$ をかけます。", isCorrect: false },
      { text: "$t = \\\\frac{s^2 - \\\\sigma_0^2}{s/\\\\sqrt{n}}$", rationale: "母分散の検定に $t$ 統計量は用いられません。$t$ 分布は母平均の検定などに用います。", isCorrect: false },
      { text: "$F = \\\\frac{s^2}{\\\\sigma_0^2}$", rationale: "2つの母分散の比の検定には $F$ 統計量を用いますが、1つの母分散の検定には $\\\\chi^2$ 統計量を用います。", isCorrect: false },
      { text: "$Z = \\\\frac{s^2 - \\\\sigma_0^2}{\\\\sigma_0^2 / \\\\sqrt{n}}$", rationale: "分散の検定では、標準正規分布 $Z$ ではなく $\\\\chi^2$ 分布に従う統計量を用います。", isCorrect: false }
    ]
  },
  {
    id: 233,
    isFormula: 1,
    category: "仮説検定",
    question: "「母比率の検定」において、標本サイズ $n$ が十分に大きい場合に用いられる検定統計量 $Z$ はどれですか？（標本比率を $\\\\hat{p}$、帰無仮説の母比率を $p_0$ とする）",
    answerOptions: [
      { text: "$Z = \\\\frac{\\\\hat{p} - p_0}{\\\\sqrt{p_0(1-p_0)/n}}$", rationale: "帰無仮説 $p = p_0$ が正しいと仮定したもとでの分散 $p_0(1-p_0)/n$ を用いて標準化します。", isCorrect: true },
      { text: "$Z = \\\\frac{\\\\hat{p} - p_0}{\\\\sqrt{\\\\hat{p}(1-\\\\hat{p})/n}}$", rationale: "分母の分散の計算に標本比率 $\\\\hat{p}$ ではなく、帰無仮説の母比率 $p_0$ を用いるのが正しい検定統計量です（区間推定の際とは異なります）。", isCorrect: false },
      { text: "$t = \\\\frac{\\\\hat{p} - p_0}{\\\\sqrt{p_0(1-p_0)/n}}$", rationale: "比率の検定では、二項分布の正規近似により $Z$ 統計量を用います。$t$ 分布は通常用いられません。", isCorrect: false },
      { text: "$Z = \\\\frac{\\\\hat{p} - p_0}{p_0(1-p_0)/\\\\sqrt{n}}$", rationale: "分母全体がルートの中に入るのが正しい形です。", isCorrect: false },
      { text: "$\\\\chi^2 = \\\\frac{(\\\\hat{p} - p_0)^2}{p_0(1-p_0)/n}$", rationale: "この式は統計量 $Z^2$ と等価であり自由度1の $\\\\chi^2$ 分布に従いますが、通常の「母比率の検定の検定統計量」の定義式としては $Z$ を選ぶのが適切です。", isCorrect: false }
    ]
  },
  {
    id: 234,
    isFormula: 1,
    category: "仮説検定",
    question: "2つの独立な標本（サイズ $n_1, n_2$、標本比率 $\\\\hat{p}_1, \\\\hat{p}_2$）による「母比率の差の検定」の検定統計量 $Z$ はどれですか？（帰無仮説 $p_1 = p_2$ のもとでのプールされた比率を $\\\\hat{p} = \\\\frac{n_1\\\\hat{p}_1 + n_2\\\\hat{p}_2}{n_1+n_2}$ とする）",
    answerOptions: [
      { text: "$Z = \\\\frac{\\\\hat{p}_1 - \\\\hat{p}_2}{\\\\sqrt{\\\\hat{p}(1-\\\\hat{p})(\\\\frac{1}{n_1} + \\\\frac{1}{n_2})}}$", rationale: "帰無仮説 $p_1 = p_2$ を仮定するため、全体の共通比率（プールされた比率）$\\\\hat{p}$ を用いて分散を計算します。", isCorrect: true },
      { text: "$Z = \\\\frac{\\\\hat{p}_1 - \\\\hat{p}_2}{\\\\sqrt{\\\\frac{\\\\hat{p}_1(1-\\\\hat{p}_1)}{n_1} + \\\\frac{\\\\hat{p}_2(1-\\\\hat{p}_2)}{n_2}}}$", rationale: "これは「母比率の差の信頼区間（区間推定）」で用いられる分散の形であり、「等しい」という帰無仮説を置く検定統計量ではありません。", isCorrect: false },
      { text: "$t = \\\\frac{\\\\hat{p}_1 - \\\\hat{p}_2}{\\\\sqrt{\\\\hat{p}(1-\\\\hat{p})(\\\\frac{1}{n_1} + \\\\frac{1}{n_2})}}$", rationale: "標本サイズが十分大きい前提の正規近似による検定のため、$t$ 統計量ではなく $Z$ 統計量を用います。", isCorrect: false },
      { text: "$Z = \\\\frac{\\\\hat{p}_1 - \\\\hat{p}_2}{\\\\hat{p}(1-\\\\hat{p})\\\\sqrt{\\\\frac{1}{n_1} + \\\\frac{1}{n_2}}}$", rationale: "分散の平方根（標準誤差）の計算式として正しくありません。$\\\\hat{p}(1-\\\\hat{p})$ もルートの中に入ります。", isCorrect: false },
      { text: "$F = \\\\frac{\\\\hat{p}_1(1-\\\\hat{p}_1)/n_1}{\\\\hat{p}_2(1-\\\\hat{p}_2)/n_2}$", rationale: "比率の差の検定に $F$ 統計量（分散の比）は用いません。", isCorrect: false }
    ]
  }"""

# Since there are exactly 2 `];` in the file (one for CATEGORIES, one for QUIZ_DATA),
# we can just use rsplit or regex with count.
# Or, even better, match the EOF using \Z or similar, but \n];\s*$ is safer.
new_text = re.sub(r'\];(\s*)$', new_questions + r'\n];\1', text)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Appended 3 new questions correctly.")
