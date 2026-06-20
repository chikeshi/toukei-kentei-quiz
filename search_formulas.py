import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

keywords = ['E(', 'E[', 'V(', 'V[', 'Cov', 'X^2', '\\sigma^2 + \\mu^2']
matches = []

for match in re.finditer(r'\{\s*id:\s*(\d+).*?question:\s*"([^"]+)".*?answerOptions:\s*\[(.*?)\]\s*\}', data, re.DOTALL):
    q_text = match.group(2)
    opts_text = match.group(3)
    # Check if any keyword is in the question or options
    for k in keywords:
        if k in q_text or k in opts_text:
            matches.append((match.group(1), q_text, opts_text[:100] + '...'))
            break

for m in matches:
    print(f"ID: {m[0]}, Q: {m[1]}")
