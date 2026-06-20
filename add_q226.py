import codecs

new_q = """  , {
    id: 226,
    isFormula: 0,
    category: "確率",
    question: "2つの確率変数 $X$ と $Y$ の間に「負の相関（共分散 $Cov(X, Y) < 0$）」がある場合、その和の分散 $V(X + Y)$ と差の分散 $V(X - Y)$ の大小関係、および公式の展開に関する記述として最も適切なものはどれですか。ただし、それぞれの分散 $V(X), V(Y)$ はともに正の値をとるものとします。",
    answerOptions: [
      { text: "$V(X + Y) < V(X - Y)$ であり、負の相関があるときは引き算のほうが分散（ばらつき）が大きくなる。", rationale: "和の分散は $V(X + Y) = V(X) + V(Y) + 2Cov(X, Y)$ 、差の分散は $V(X - Y) = V(X) + V(Y) - 2Cov(X, Y)$ と展開されます。負の相関がある場合、共分散 $Cov(X, Y)$ は負の値になります。そのため、和の分散では値が引き算されて小さくなり、差の分散ではマイナスとマイナスが打ち消し合ってプラス（加算）されるため、必ず $V(X + Y) < V(X - Y)$ となります。", isCorrect: true },
      { text: "$V(X + Y) > V(X - Y)$ であり、いかなる相関関係であっても和の分散のほうが必ず大きくなる。", rationale: "正の相関（$Cov(X, Y) > 0$）がある場合は和の分散の方が大きくなりますが、いかなる場合でも必ず大きくなるわけではありません。", isCorrect: false },
      { text: "$V(X + Y) > V(X - Y)$ であり、負の相関があるときは足し算のほうが分散（ばらつき）が大きくなる。", rationale: "和の分散の展開式に含まれる $+ 2Cov(X, Y)$ は、負の相関の場合マイナスの値をとるため、ばらつきは小さくなります。", isCorrect: false },
      { text: "$V(X + Y) < V(X - Y)$ であるが、負の相関の強さによっては $V(X + Y)$ のほうが大きくなることもある。", rationale: "負の相関（$Cov(X, Y) < 0$）である限り、必ず $V(X + Y) < V(X - Y)$ となるため、相関の強さによって大小関係が逆転することはありません。", isCorrect: false }
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
    print("Added new question 226 successfully.")
else:
    print("Could not find the end of the array.")
