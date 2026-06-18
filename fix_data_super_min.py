import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# ID 163
data = re.sub(r'\$E\(aX \+ bY\) = aE\(X\) \+ bE\(Y\)\$[^\"]*独立[^"]*限る[^\"]*\"', r'$E(aX + bY) = a^2 E(X) + b^2 E(Y)$"', data)

# ID 71
data = data.replace(r'1.64 \sqrt{\frac{p(1-p)}{n}}', r'1.96 \sqrt{\frac{p}{n}}')
data = data.replace(r'1.64 \\sqrt{\\frac{p(1-p)}{n}}', r'1.96 \\sqrt{\\frac{p}{n}}')

# ID 75
data = data.replace(r'\sqrt{ラスパイレス指数 \times パーシェ指数}', r'\frac{\sum p_0 q_0}{\sum p_t q_t} \times 100')
data = data.replace(r'\\sqrt{ラスパイレス指数 \\times パーシェ指数}', r'\\frac{\\sum p_0 q_0}{\\sum p_t q_t} \\times 100')

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(data)

print("Super minimal replacements done.")
