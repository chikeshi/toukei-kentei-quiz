import codecs
import re

new_text = codecs.open('data.js', 'r', 'utf-8').read()
cats = set(re.findall(r'category:\s*"([^"]+)"', new_text))
print("Categories found using utf-8:")
for c in cats:
    print(c)
    print("Does it equal 確率・確率分布?", c == "確率・確率分布")
    print("Does it equal 推測統計?", c == "推測統計")
