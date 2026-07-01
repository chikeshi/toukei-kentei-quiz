import codecs

text = codecs.open('data.js', 'r', 'utf-8').read()

replacements = [
    (r'text: "$aV(X) + b$"(.*?isCorrect: false)', r'text: "$a V(X) - b$"\1'),
    (r'text: "$\\\\bar{x} \\\\pm 1.96 \\\\sigma$"(.*?rationale: ".*?母集団の標準偏差.*?")', r'text: "$\\bar{x} \\pm \\sigma$"\1'), # Only match the specific duplicate
    (r'text: "$\\\\hat{\\\\beta}_1 = \\\\frac{S_{xy}}{\\\\sqrt{S_{xx} S_{yy}}}$"(.*?isCorrect: false)', r'text: "$\\hat{\\beta}_1 = \\frac{S_{xx}}{\\sqrt{S_{xx} S_{yy}}}$"\1'),
    (r'text: "$\(r-1\) \+ \(c-1\)$"(.*?rationale: ".*?周辺和.*?")', r'text: "$r \\times c - 2$"\1'),
    (r'text: "\$aV\(X\) \+ bV\(Y\) \+ 2Cov\(X,Y\)\$"(.*?isCorrect: false)', r'text: "$a^2 V(X) + b^2 V(Y) - ab Cov(X,Y)$"\1'),
    (r'text: "\$E\\\\left\[\\\\left\(\\\\frac\{X-\\\\mu\}\{\\\\sigma\}\\\\right\)\^4\\\\right\]\$"(.*?rationale: ".*?歪度.*?")', r'text: "$E\\left[ \\left( \\frac{X-\\mu}{\\sigma} \\right)^2 \\right]^2$"\1'),
    (r'text: "\$\\\\frac\{S_E / \(n - a\)\}\{S_A / \(a - 1\)\}\$"(.*?isCorrect: false)', r'text: "$\\frac{S_E / a}{S_A / n}$"\1'),
    (r'text: "\$\\\\frac\{r_\{xy\} - r_\{xz\}r_\{yz\}\}\{1 - r_\{xz\}r_\{yz\}\}\$"(.*?isCorrect: false)', r'text: "$\\frac{r_{xy} - r_{xz} r_{yz}}{1 - r_{xz}^2 r_{yz}^2}$"\1')
]

import re
for pat, repl in replacements:
    text = re.sub(pat, repl, text, count=1, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(text)

print("Duplicates fixed!")
