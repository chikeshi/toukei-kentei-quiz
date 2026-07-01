import codecs
import re

with codecs.open('quiz_updated.js', 'r', 'utf-8') as f:
    js = f.read()

# Hook up btnPrev event listener
replacement = "$('btnNext').addEventListener('click', handleNext);\n$('btnPrev').addEventListener('click', handlePrev);"
js = js.replace("$('btnNext').addEventListener('click', handleNext);", replacement)

# Overwrite original quiz.js
with codecs.open('quiz.js', 'w', 'utf-8') as f:
    f.write(js)
