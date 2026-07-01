import json
import math

with open('questions_dump.json', 'r', encoding='utf-8') as f:
    qs = json.load(f)

chunk_size = math.ceil(len(qs) / 4)

for i in range(4):
    chunk = qs[i * chunk_size : (i + 1) * chunk_size]
    with open(f'part_{i}.json', 'w', encoding='utf-8') as f:
        json.dump(chunk, f, ensure_ascii=False, indent=2)
    print(f'Wrote part_{i}.json with {len(chunk)} questions.')
