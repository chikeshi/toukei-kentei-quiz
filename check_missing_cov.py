import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

for q in ["Cov(X, X)", "Cov[X, X]", "acCov", "Cov(X+Y, Z)"]:
    if q in data:
        print(f"Found {q}")
    else:
        print(f"Missing {q}")
