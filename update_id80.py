import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()

new_opts = """    answerOptions: [
      { text: "$F = \\\\frac{s_1^2}{s_2^2}$", rationale: "2つの母分散の比に関する検定（等分散の検定）には、2つの標本不偏分散の比であるF統計量を用います。帰無仮説（等分散）のもとで自由度 $(n_1-1, n_2-1)$ のF分布に従います。", isCorrect: true },
      { text: "$F = \\\\frac{s_1^2(n_1-1)}{s_2^2(n_2-1)}$", rationale: "分子分母に $(n-1)$ をかけているため、これは不偏分散の比ではなく「標本平方和の比」になってしまいます。F統計量は不偏分散の比を用います。", isCorrect: false },
      { text: "$\\\\chi^2 = \\\\frac{s_1^2}{s_2^2}$", rationale: "2つの分散の比は $\\\\chi^2$ 統計量ではなく、F統計量となります。$\\\\chi^2$ 統計量は1つの母分散の検定などに用いられます。", isCorrect: false },
      { text: "$\\\\chi^2 = \\\\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{\\\\sigma^2}$", rationale: "これは等分散を仮定した際のプールされた分散に関連する式であり、等分散かどうかの検定（分散の比の検定）の検定統計量ではありません。", isCorrect: false },
      { text: "$F = \\\\frac{s_1^2 / n_1}{s_2^2 / n_2}$", rationale: "標本サイズ $n$ で割っているため誤りです。標本平均の分散（平均の差の検定など）の計算で出てくる形と混同した引掛けです。", isCorrect: false }
    ]"""

# Replace the answerOptions array for ID 80
def replace_id_80(match):
    before = match.group(1)
    return before + new_opts

new_text = re.sub(r'(id:\s*80,.*?)(answerOptions:\s*\[.*?\])', replace_id_80, text, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("ID 80 replaced.")
