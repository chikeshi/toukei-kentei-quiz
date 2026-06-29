import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

ids_to_dump = [214, 208, 125, 171]

with codecs.open('dump_ids_post.txt', 'w', 'utf-8') as f_out:
    for target_id in ids_to_dump:
        m = re.search(r'\{\s*id:\s*' + str(target_id) + r'\b.*?\s*answerOptions:\s*\[.*?\]\s*\}', data, re.DOTALL)
        if m:
            f_out.write(m.group(0) + '\n\n')
        else:
            f_out.write(f"ID {target_id} not found\n\n")
