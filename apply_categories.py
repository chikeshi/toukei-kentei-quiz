import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Update the CATEGORIES array
new_categories_str = """const CATEGORIES = [
  { name: "記述統計・基礎", desc: "グラフ、代表値、サンプリング手法、季節変動、ラスパイレス式等", icon: "📊" },
  { name: "確率・確率分布", desc: "ベイズ、条件付き確率、正規分布、二項分布、ポアソン分布、t/F/χ²分布", icon: "🎲" },
  { name: "推測統計", desc: "推定、仮説検定、過誤、P値", icon: "🔬" },
  { name: "回帰分析・分散分析", desc: "単回帰、重回帰、決定係数、分散分析", icon: "📉" }
];"""

data = re.sub(r'const CATEGORIES = \[.*?\];', new_categories_str, data, flags=re.DOTALL)

def find_objects(data_str):
    objects = []
    idx = data_str.find('const QUIZ_DATA = [') + len('const QUIZ_DATA = [')
    while True:
        start = data_str.find('{', idx)
        if start == -1: break
        depth = 0
        in_string = False
        escape = False
        str_char = ''
        end = -1
        for i in range(start, len(data_str)):
            c = data_str[i]
            if not in_string:
                if c == '{': depth += 1
                elif c == '}': 
                    depth -= 1
                    if depth == 0:
                        end = i
                        break
                elif c in ('"', "'", '`'):
                    in_string = True
                    str_char = c
            else:
                if escape: escape = False
                elif c == '\\': escape = True
                elif c == str_char: in_string = False
        
        if end != -1:
            objects.append(data_str[start:end+1])
            idx = end + 1
        else:
            break
    return objects

objects = find_objects(data)
new_objects = []

for obj_str in objects:
    # Get current category
    cat_match = re.search(r'category:\s*"(.*?)"', obj_str)
    if not cat_match:
        new_objects.append(obj_str)
        continue
    
    cat = cat_match.group(1)
    new_cat = cat
    
    if cat == "時系列・指数":
        new_cat = "記述統計・基礎"
    elif cat in ["確率", "確率分布"]:
        new_cat = "確率・確率分布"
    elif cat == "線形モデル":
        new_cat = "回帰分析・分散分析"
    
    # If it's related to ANOVA, move to 回帰分析・分散分析
    if '分散分析' in obj_str or '一元配置' in obj_str or '二元配置' in obj_str:
        new_cat = "回帰分析・分散分析"

    if new_cat != cat:
        # replace category name
        obj_str = re.sub(r'category:\s*".*?"', f'category: "{new_cat}"', obj_str, count=1)
        
    new_objects.append(obj_str)

final_text = data[:data.find('const QUIZ_DATA = [')] + "const QUIZ_DATA = [\n  " + ",\n  ".join(new_objects) + "\n];\n"

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(final_text)

print("Categorization update applied.")
