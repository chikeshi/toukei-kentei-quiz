import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()
# Replace ALL non-ascii characters with "X"
text = re.sub(r'[^\x00-\x7F]+', 'X', text)
text = text.replace('const CATEGORIES', 'var CATEGORIES').replace('const QUIZ_DATA', 'var QUIZ_DATA')

with codecs.open('check_no_emoji.js', 'w', 'utf-8') as f:
    f.write(text)
    f.write('\n\nWScript.Echo("Syntax is OK!");\n')
