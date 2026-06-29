import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

m = re.search(r'\{\s*id:\s*171\b.*?\s*answerOptions:\s*\[.*?\]\s*\}', data, re.DOTALL)
if m:
    obj_str = m.group(0)
    # The current obj_str has single backslashes like \hat, \bar, \frac, \beta
    # We need to replace \h with \\h, \b with \\b, \f with \\f
    # But wait, python might have already parsed \b as backspace?
    # Let's see what is actually in the file.
    
    # It's safer to just rebuild the object for 171 correctly.
    new_obj_str = """  {
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
    
    new_data = data.replace(obj_str, new_obj_str)
    with codecs.open('data.js', 'w', 'utf-8') as f:
        f.write(new_data)
    print("Fixed ID 171 backslashes.")
else:
    print("ID 171 not found.")
