import codecs
import re
from collections import Counter

text = codecs.open('data.js', 'r', 'utf-8').read()
blocks = re.split(r'(?=\{\s*id:\s*)', text)
new_blocks = [blocks[0]]

# Map of ID to the duplicate text, and the replacement text for the INCORRECT option.
replacements = {
    54: ('$P(A) \\times P(B)$', '$P(A) + P(B) - 2P(A \\cap B)$'),
    68: ('$\\bar{x} \\pm 1.96 \\sigma$', '$\\bar{x} \\pm 1.96 \\frac{\\sigma}{\\sqrt{n-1}}$'),
    71: ('$\\hat{p} \\pm 1.96 \\frac{\\hat{p}(1-\\hat{p})}{\\sqrt{n}}$', '$\\hat{p} \\pm 1.96 \\frac{\\hat{p}(1-\\hat{p})}{n}$'),
    72: ('$\\hat{\\beta}_1 = \\frac{S_{xx}}{S_{xy}}$', '$\\hat{\\beta}_1 = \\frac{S_{xy}}{\\sqrt{S_{xx}S_{yy}}}$'),
    74: ('$r = \\frac{S_{xy}}{S_{xx} S_{yy}}$', '$r = \\frac{S_{xy}^2}{S_{xx} S_{yy}}$'),
    87: ('$R^{*2} = R^2 - \\frac{k}{n}$', '$R^{*2} = 1 - \\frac{k}{n}R^2$'),
    91: ('$s^2 = \\frac{s_1^2 + s_2^2}{2}$', '$s^2 = \\frac{n_1 s_1^2 + n_2 s_2^2}{n_1 + n_2 - 2}$'),
    95: ('$\\sum \\frac{(O_i - E_i)^2}{O_i}$', '$\\sum \\frac{(O_i - E_i)^2}{E_i^2}$'),
    96: ('$r \\times c - 1$', '$(r-1) + (c-1)$'),
    130: ('$\\frac{SE(\\hat{\\beta}_j)}{\\hat{\\beta}_j}$', '$\\frac{\\hat{\\beta}_j}{SE(\\hat{\\beta}_j)^2}$'),
    212: ('$E[XY] + E[X]E[Y]$', '$E[X+Y] - E[X]E[Y]$'),
    233: ('$\\frac{\\hat{p} - p_0}{\\sqrt{p_0(1-p_0)/n}}$', '$\\frac{\\hat{p} - p_0}{\\sqrt{p_0(1-p_0)/(n-1)}}$'),
    234: ('$\\frac{\\hat{p}_1 - \\hat{p}_2}{\\sqrt{\\hat{p}(1-\\hat{p})(\\frac{1}{n_1} + \\frac{1}{n_2})}}$', '$\\frac{\\hat{p}_1 - \\hat{p}_2}{\\sqrt{\\hat{p}(1-\\hat{p})(\\frac{1}{n_1-1} + \\frac{1}{n_2-1})}}$')
}

for b in blocks[1:]:
    id_m = re.search(r'id:\s*(\d+)', b)
    if not id_m:
        new_blocks.append(b)
        continue
    qid = int(id_m.group(1))
    
    if qid in replacements:
        dup_text, new_text = replacements[qid]
        
        # We need to find the option that has text: "dup_text" AND isCorrect: false
        # The structure is: { text: "dup_text", rationale: "...", isCorrect: false }
        # Because we only want to change the FALSE one, not the correct one.
        
        # We'll split the block into lines, and when we see `text: "dup_text"`, we check the rest of the object.
        # A simpler way is to use regex with lookahead/lookbehind or just findall the option blocks.
        
        option_pattern = re.compile(r'(\{\s*text:\s*")(.*?)(".*?isCorrect:\s*)(true|false)(\s*\})', re.DOTALL)
        
        def option_repl(m):
            t = m.group(2)
            is_correct = m.group(4) == 'true'
            # If this is the duplicate text and it's the wrong answer, replace the text
            if t.replace('\\\\', '\\') == dup_text.replace('\\\\', '\\') and not is_correct:
                return m.group(1) + new_text.replace('\\', '\\\\') + m.group(3) + m.group(4) + m.group(5)
            # Actually, because reading python string vs writing python string backslashes can be tricky,
            # Let's just compare raw string literally.
            # In the file, backslashes are literal.
            
            # Since backslashes in data.js are literal (e.g. \\hat), we should compare carefully.
            # Let's just do a simpler replacement.
            return m.group(0)
            
        # Instead of the complex regex above which might miss due to backslashes, let's just do:
        # find the duplicate string in the file (e.g. `text: "$\\frac...$"`).
        
        # Let's extract the exact string from the file first.
        opts = re.findall(r'text:\s*"(.*?)"', b)
        c = Counter(opts)
        dups = [k for k,v in c.items() if v > 1]
        
        if dups:
            dup = dups[0]
            # Replace the ONE that is accompanied by `isCorrect: false`
            # We split `b` by the duplicate text, and we look at the part following it.
            parts = b.split(f'text: "{dup}"')
            new_b = parts[0]
            replaced = False
            for i in range(1, len(parts)):
                if not replaced and 'isCorrect: false' in parts[i].split('}')[0]:
                    # This is the wrong option
                    new_b += f'text: "{new_text.replace(chr(92), chr(92)+chr(92))}"' + parts[i]
                    replaced = True
                else:
                    new_b += f'text: "{dup}"' + parts[i]
            b = new_b
            
    new_blocks.append(b)

new_text = ''.join(new_blocks)
with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_text)

print("Duplicates fixed!")
