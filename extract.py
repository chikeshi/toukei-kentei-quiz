import codecs

with codecs.open('quiz.js', 'r', 'utf-8') as f:
    lines = f.readlines()

# Line 26 is index 25, line 529 is index 528.
data_lines = lines[25:529]
quiz_lines = lines[:25] + lines[529:]

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.writelines(data_lines)

with codecs.open('quiz.js', 'w', 'utf-8') as f:
    f.writelines(quiz_lines)

print("Extraction complete.")
