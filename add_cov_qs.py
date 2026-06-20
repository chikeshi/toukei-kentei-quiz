import codecs

new_qs = """  , {
    id: 227,
    isFormula: 1,
    category: "確率",
    question: "確率変数 $X$ について、自分自身との共分散 $Cov(X, X)$ を表す式として最も適切なものはどれですか？",
    answerOptions: [
      { text: "$V(X)$", rationale: "$Cov(X,X) = E[(X-E[X])(X-E[X])] = E[(X-E[X])^2] = V(X)$ となり、自分自身との共分散は分散と等しくなります。", isCorrect: true },
      { text: "$E(X)^2$", rationale: "$V(X) = E(X^2) - \\{E(X)\\}^2$ なので異なります。", isCorrect: false },
      { text: "$1$", rationale: "相関係数 $r(X,X)$ であれば $1$ になりますが、共分散は分散に等しくなります。", isCorrect: false },
      { text: "$0$", rationale: "確率変数が定数でない限り、分散は $0$ より大きな値をとります。", isCorrect: false }
    ]
  }, {
    id: 228,
    isFormula: 1,
    category: "確率",
    question: "確率変数 $X, Y$ と定数 $a, b, c, d$ について、共分散 $Cov(aX + b, cY + d)$ を展開した式として正しいものはどれですか？",
    answerOptions: [
      { text: "$ac Cov(X, Y)$", rationale: "共分散は定数の加算 ($+b, +d$) に影響されず、乗算された定数 ($a, c$) はそのまま外に出ます。", isCorrect: true },
      { text: "$ac Cov(X, Y) + bd$", rationale: "分散や共分散において、足された定数項 ($+b, +d$) はばらつきに影響しないため無視されます。", isCorrect: false },
      { text: "$a Cov(X, Y) + c Cov(X, Y)$", rationale: "各変数の係数は足し算ではなく掛け合わせる必要があります。", isCorrect: false },
      { text: "$a^2 c^2 Cov(X, Y)$", rationale: "分散 $V(aX) = a^2 V(X)$ とは異なり、共分散の係数は2乗されずそのまま $a \\times c$ となります。", isCorrect: false }
    ]
  }, {
    id: 229,
    isFormula: 1,
    category: "確率",
    question: "確率変数 $X, Y, Z$ について、和と別の確率変数との共分散 $Cov(X + Y, Z)$ を展開した式として正しいものはどれですか？",
    answerOptions: [
      { text: "$Cov(X, Z) + Cov(Y, Z)$", rationale: "共分散は線形性を持つため、分配法則のように足し算で展開することができます。", isCorrect: true },
      { text: "$Cov(X, Z) \\times Cov(Y, Z)$", rationale: "足し算が掛け算になることはありません。", isCorrect: false },
      { text: "$V(X) + V(Y) + 2Cov(X, Y)$", rationale: "これは和の分散 $V(X+Y)$ の展開式であり、無関係の式です。", isCorrect: false },
      { text: "$Cov(X, Z) + Cov(Y, Z) + Cov(X, Y)$", rationale: "展開時に $X$ と $Y$ の共分散は発生しません。", isCorrect: false }
    ]
  }"""

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

idx = data.rfind(']')
if idx != -1:
    new_data = data[:idx] + new_qs + '\n' + data[idx:]
    with codecs.open('data.js', 'w', 'utf-8') as f:
        f.write(new_data)
    print("Added 3 new covariance questions successfully.")
else:
    print("Could not find the end of the array.")
