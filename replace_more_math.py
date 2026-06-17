import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

more_replacements = {
    r"s_1^2/n_1": r"\frac{s_1^2}{n_1}",
    r"s_2^2/n_2": r"\frac{s_2^2}{n_2}",
    r"x_1/n_1": r"\frac{x_1}{n_1}",
    r"x_2/n_2": r"\frac{x_2}{n_2}",
    r"s_p \sqrt{1/n_1 + 1/n_2}": r"s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}",
    r"s_p \sqrt{1/n_1 + 1/n_2}": r"s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}",
    r"(\bar{x}_1 - \bar{x}_2) \pm Z_{\alpha/2} \times s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}": r"(\bar{x}_1 - \bar{x}_2) \pm Z_{\alpha/2} \times s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}", # already frac? Wait, in my dump: s_p \sqrt{1/n_1 + 1/n_2}
    r"(\bar{x}_1 - \bar{x}_2) \pm t_{\alpha/2} \times \frac{s_p}{\sqrt{n_1 + n_2}}": r"(\bar{x}_1 - \bar{x}_2) \pm t_{\alpha/2} \times \frac{s_p}{\sqrt{n_1 + n_2}}", # already frac, skip
}

def replacer(m):
    expr = m.group(1)
    lookup_expr = expr.replace(r'\\', '\\')
    
    if lookup_expr in more_replacements:
        new_expr = more_replacements[lookup_expr].replace('\\', r'\\')
        return "$" + new_expr + "$"
        
    lookup_expr_stripped = lookup_expr.strip()
    if lookup_expr_stripped in more_replacements:
        new_expr = more_replacements[lookup_expr_stripped].replace('\\', r'\\')
        return "$ " + new_expr + " $" if expr.startswith(' ') else "$" + new_expr + "$"
        
    return m.group(0)

new_data = re.sub(r'\$(.*?)\$', replacer, data)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("More replacements complete.")
