import codecs
import re

old_text = codecs.open('old_data_clean.js', 'r', 'utf-8').read()
new_text = codecs.open('data.js', 'r', 'utf-8').read()

# Extract old categories map
old_cat_map = {}
old_blocks = old_text.split('\n  {\n    id: ')
for b in old_blocks[1:]:
    id_match = re.search(r'^(\d+),', b)
    cat_match = re.search(r'category:\s*"([^"]+)"', b)
    if id_match and cat_match:
        old_cat_map[int(id_match.group(1))] = cat_match.group(1)

print("Old cat map size:", len(old_cat_map))

# Helper to classify 推測統計
def classify_inference(text):
    text = text.lower()
    hypothesis_keywords = ['検定', '帰無仮説', '対立仮説', '有意', '棄却', 'p値', '過誤', '検出力']
    for kw in hypothesis_keywords:
        if kw in text:
            return "仮説検定"
    return "推定"

# Now parse the current data.js to update categories
new_blocks = new_text.split('\n  {\n    id: ')
updated_blocks = [new_blocks[0]]

counts = {"確率分布":0, "確率":0, "推定":0, "仮説検定":0}

for b in new_blocks[1:]:
    id_match = re.search(r'^(\d+),', b)
    if not id_match:
        updated_blocks.append(b)
        continue
    
    q_id = int(id_match.group(1))
    
    # Extract the question text to classify 推測統計
    q_match = re.search(r'question:\s*"([^"]+)"', b)
    q_text = q_match.group(1) if q_match else ""
    
    # Get current category
    cat_match = re.search(r'category:\s*"([^"]+)"', b)
    if not cat_match:
        updated_blocks.append(b)
        continue
        
    current_cat = cat_match.group(1)
    new_cat = current_cat
    
    # Since my previous script corrupted them to "確率分布", "推定", "仮説検定",
    # we need to check if it's ANY of those, AND check the old map.
    if current_cat in ["確率・確率分布", "確率分布", "確率"]:
        if q_id in old_cat_map:
            new_cat = old_cat_map[q_id]
            if new_cat not in ["確率", "確率分布"]:
                new_cat = "確率分布"
        else:
            new_cat = "確率分布"
    elif current_cat in ["推測統計", "推定", "仮説検定"]:
        # Re-classify just in case
        new_cat = classify_inference(q_text)
        
    if new_cat in counts:
        counts[new_cat] += 1
        
    # Replace the category in the block
    b_updated = re.sub(r'category:\s*"[^"]+"', f'category: "{new_cat}"', b)
    updated_blocks.append(b_updated)
    
cat_array = """const CATEGORIES = [
  { name: "記述統計・基礎", desc: "グラフ、代表値、サンプリング手法、季節変動、ラスパイレス式等", icon: "📊" },
  { name: "確率", desc: "ベイズの定理、条件付き確率、事象の独立など", icon: "🎲" },
  { name: "確率分布", desc: "正規分布、二項分布、ポアソン分布、t/F/χ²分布、期待値と分散", icon: "📈" },
  { name: "推定", desc: "点推定、区間推定、信頼区間、不偏推定量", icon: "🎯" },
  { name: "仮説検定", desc: "帰無仮説、有意水準、P値、各種検定", icon: "⚖️" },
  { name: "回帰分析・分散分析", desc: "単回帰、重回帰、決定係数、分散分析表", icon: "📉" }
];"""

final_text = '\n  {\n    id: '.join(updated_blocks)
final_text = re.sub(r'const\s+CATEGORIES\s*=\s*\[.*?\];', cat_array, final_text, flags=re.DOTALL)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(final_text)

print("Categories remapped successfully.", counts)
