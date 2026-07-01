import codecs

text = codecs.open('quiz.js', 'r', 'utf-8').read()
# We can't run quiz.js in JScript easily because it uses const, let, arrow functions.
# But we can try to use python's ast to parse it if we convert it to python? No.
# Is there ANY javascript parser in python standard library? No.
