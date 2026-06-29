import subprocess
import codecs

out = subprocess.check_output(['git', 'show', '0afcdde:data.js']).decode('utf-8')
with codecs.open('top.txt', 'w', 'utf-8') as f:
    f.write(out[:1000])
