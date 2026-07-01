import codecs
import re

text = codecs.open('data.js', 'r', 'utf-8').read()
text = text.replace('const CATEGORIES', 'var CATEGORIES').replace('const QUIZ_DATA', 'var QUIZ_DATA')

with codecs.open('check.js', 'w', 'utf-8') as f:
    f.write(text)
    f.write('\n\nWScript.Echo("Syntax is OK!");\n')
