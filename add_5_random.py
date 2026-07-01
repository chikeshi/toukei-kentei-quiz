import codecs
import re

# UPDATE INDEX.HTML
with codecs.open('index.html', 'r', 'utf-8') as f:
    html = f.read()

# We need to find the <button id="btnStart10"... block
# It starts with <button id="btnStart10" and ends with </button>
match = re.search(r'<button id="btnStart10".*?</button>', html, re.DOTALL)
if match:
    btn10_str = match.group(0)
    btn5_str = btn10_str.replace('btnStart10', 'btnStart5').replace('10問抽出', '5問抽出')
    new_html = html[:match.start()] + btn5_str + '\n            ' + btn10_str + html[match.end():]
    new_html = new_html.replace('data.js?v=1.22', 'data.js?v=1.24')
    new_html = new_html.replace('quiz.js?v=1.5', 'quiz.js?v=1.6')
    
    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(new_html)
    print("Updated index.html")
else:
    print("Could not find btnStart10 in index.html")

# UPDATE QUIZ.JS
with codecs.open('quiz.js', 'r', 'utf-8') as f:
    js = f.read()

js = re.sub(r'isRandom10:\s*false,', 'randomLimit: 0,', js)
js = js.replace('function startQuiz(isRandom10 = false) {', 'function startQuiz(randomLimit = 0) {')
js = js.replace('state.isRandom10 = isRandom10;', 'state.randomLimit = randomLimit;')
js = js.replace('if (state.isRandom10 && shuffled.length > 10) {', 'if (state.randomLimit > 0 && shuffled.length > state.randomLimit) {')
js = js.replace('shuffled = shuffled.slice(0, 10);', 'shuffled = shuffled.slice(0, state.randomLimit || 10);')

js = js.replace("startQuiz(false)", "startQuiz(0)")
js = js.replace("startQuiz(true)", "startQuiz(10)")

js = js.replace("if ($('btnStart10')) $('btnStart10').disabled = catCount === 0;",
                "if ($('btnStart10')) $('btnStart10').disabled = catCount === 0;\n  if ($('btnStart5')) $('btnStart5').disabled = catCount === 0;")

listener_code = """if ($('btnStart10')) {
  $('btnStart10').addEventListener('click', () => startQuiz(10));
}"""

new_listener_code = """if ($('btnStart5')) {
  $('btnStart5').addEventListener('click', () => startQuiz(5));
}
if ($('btnStart10')) {
  $('btnStart10').addEventListener('click', () => startQuiz(10));
}"""

if "if ($('btnStart10')) {" in js:
    js = re.sub(r"if \(\$\('btnStart10'\)\) \{\s*\$\('btnStart10'\)\.addEventListener\('click', \(\) => startQuiz\(.*?\)\);\s*\}", new_listener_code, js)

with codecs.open('quiz.js', 'w', 'utf-8') as f:
    f.write(js)

print("Updated quiz.js")
