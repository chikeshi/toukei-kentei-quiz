import codecs

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

idx = data.find('}_0 + \\\\hat{\\\\beta}_1')
if idx != -1:
    with codecs.open('error_context.txt', 'w', 'utf-8') as f:
        f.write(data[max(0, idx-200):min(len(data), idx+200)])
    print("Found and exported context to error_context.txt")
else:
    print("Not found!")
