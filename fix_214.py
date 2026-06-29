import codecs

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Fix the single backslashes in ID 214 that got mangled by re.sub
data = data.replace('\\int_{-\\infty}^{\\infty} (x - \\mu)', '\\\\int_{-\\\\infty}^{\\\\infty} (x - \\\\mu)')

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(data)

print("Fixed ID 214 backslashes.")
