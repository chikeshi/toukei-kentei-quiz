import codecs

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

categories_str = """const CATEGORIES = [
  { name: "記述統計・基礎", desc: "グラフ、代表値、サンプリング手法", icon: "📊" },
  { name: "確率", desc: "ベイズ、条件付き確率", icon: "🎲" },
  { name: "確率分布", desc: "正規分布、二項分布、ポアソン分布、t/F/χ²分布", icon: "📈" },
  { name: "推測統計", desc: "推定、仮説検定、過誤、P値", icon: "🔬" },
  { name: "線形モデル", desc: "単回帰、重回帰、決定係数", icon: "📉" },
  { name: "時系列・指数", desc: "季節変動、ラスパイレス式等", icon: "🕐" },
];

"""

if "const CATEGORIES" not in data:
    with codecs.open('data.js', 'w', 'utf-8') as f:
        f.write(categories_str + data)
    print("CATEGORIES restored!")
else:
    print("CATEGORIES already present.")
