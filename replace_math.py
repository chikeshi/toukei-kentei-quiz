import codecs
import re

with codecs.open('data.js', 'r', 'utf-8') as f:
    data = f.read()

# Exact full-string replacements for math expressions.
# We only replace expressions that are exactly matching these.

exact_math_replacements = {
    # Replacements explicitly requested or obvious 1-level fractions
    r"(1-p)/p^2": r"\frac{1-p}{p^2}",
    r"(N-n)/(N-1)": r"\frac{N-n}{N-1}",
    r"(\bar{x} - \mu_0) / (\sigma / \sqrt{n})": r"\frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}",
    r"(\bar{x} - \mu_0) / (s / \sqrt{n})": r"\frac{\bar{x} - \mu_0}{s / \sqrt{n}}",
    r"(\bar{x}_1 - \bar{x}_2) / SE": r"\frac{\bar{x}_1 - \bar{x}_2}{SE}",
    r"(a+b)/2": r"\frac{a+b}{2}",
    r"(n-1)s^2 / \sigma^2": r"\frac{(n-1)s^2}{\sigma^2}",
    r"1/(b-a)": r"\frac{1}{b-a}",
    r"1/(n-3)": r"\frac{1}{n-3}",
    r"1/2": r"\frac{1}{2}",
    r"1/6": r"\frac{1}{6}",
    r"1/\lambda": r"\frac{1}{\lambda}",
    r"1/\lambda^2": r"\frac{1}{\lambda^2}",
    r"1/\sqrt{2\pi\sigma^2} \exp \{-(x-\mu)^2 / (2\sigma^2)\}": r"\frac{1}{\sqrt{2\pi\sigma^2}} \exp \left\{ -\frac{(x-\mu)^2}{2\sigma^2} \right\}",
    r"1/\sqrt{2\pi} \exp \{-x^2 / 2\}": r"\frac{1}{\sqrt{2\pi}} \exp \left\{ -\frac{x^2}{2} \right\}",
    r"1/\sqrt{2} \approx 0.71": r"\frac{1}{\sqrt{2}} \approx 0.71",
    r"1/k^2": r"\frac{1}{k^2}",
    r"1/p": r"\frac{1}{p}",
    r"P(A \cap B) / P(A)": r"\frac{P(A \cap B)}{P(A)}",
    r"P(A \cap B) / P(B)": r"\frac{P(A \cap B)}{P(B)}",
    r"P(A) / P(B|A)": r"\frac{P(A)}{P(B|A)}",
    r"P(B|A) = P(A \cap B) / P(A)": r"P(B|A) = \frac{P(A \cap B)}{P(A)}",
    r"P(X \ge a) \le E(X)/a": r"P(X \ge a) \le \frac{E(X)}{a}",
    r"S_{xy} / \sqrt{S_{xx} S_{yy}}": r"\frac{S_{xy}}{\sqrt{S_{xx} S_{yy}}}",
    r"\bar{d} / (s_d / \sqrt{n})": r"\frac{\bar{d}}{s_d / \sqrt{n}}",
    r"\hat{p} = X/n": r"\hat{p} = \frac{X}{n}",
    r"\hat{p}(1-\hat{p})/n": r"\frac{\hat{p}(1-\hat{p})}{n}",
    r"\sigma / \sqrt{n}": r"\frac{\sigma}{\sqrt{n}}",
    r"\sigma/\sqrt{n}": r"\frac{\sigma}{\sqrt{n}}",
    r"\sigma_1^2 / \sigma_2^2": r"\frac{\sigma_1^2}{\sigma_2^2}",
    r"\sum (O - E) / E": r"\frac{\sum (O - E)}{E}",
    r"\sum (O - E)^2 / E": r"\frac{\sum (O - E)^2}{E}",
    r"\sum (O - E)^2 / O": r"\frac{\sum (O - E)^2}{O}",
    r"\sum(O-E)^2 / E": r"\frac{\sum(O-E)^2}{E}",
    r"\theta = 1/\lambda": r"\theta = \frac{1}{\lambda}",
    r"e^{-\lambda} \lambda^x / x!": r"\frac{e^{-\lambda} \lambda^x}{x!}",
    r"k \approx n / \log_{10} n": r"k \approx \frac{n}{\log_{10} n}",
    r"n/p": r"\frac{n}{p}",
    r"p(1-p)/n": r"\frac{p(1-p)}{n}",
    r"s/\sqrt{n}": r"\frac{s}{\sqrt{n}}",
    r"t = (\bar{d} - 0) / (s_d / \sqrt{n})": r"t = \frac{\bar{d} - 0}{s_d / \sqrt{n}}",
    
    # We also have "E(X) = 1/\lambda, \quad V(X) = 1/\lambda^2"
    r"E(X) = 1/\lambda, \quad V(X) = 1/\lambda^2": r"E(X) = \frac{1}{\lambda}, \quad V(X) = \frac{1}{\lambda^2}",
    r"E(X) = p, \quad V(X) = p(1-p)/n": r"E(X) = p, \quad V(X) = \frac{p(1-p)}{n}",
    
    r"V(X/n) = V(X)/n^2": r"V(X/n) = \frac{V(X)}{n^2}",
    
    # Wait, there are text strings with formulas: "s / \sqrt{n}" in text.
    # Let's write them properly. Wait, if it's inside `$...$`, it will be replaced.
    r"s / \sqrt{n}": r"\frac{s}{\sqrt{n}}",
}

def replacer(m):
    expr = m.group(1)
    # Javascript has double backslashes, but re.findall over raw strings un-escapes them if we don't be careful?
    # Wait! If data is read via codecs.open, the literal string is `\\sigma`.
    # Let's decode them before lookup, then encode back.
    # Actually, we can just replace the string `m.group(1)` by removing double slashes to single slashes for lookup!
    lookup_expr = expr.replace(r'\\', '\\')
    
    if lookup_expr in exact_math_replacements:
        # replace with the mapped value, and double-escape the backslashes
        new_expr = exact_math_replacements[lookup_expr].replace('\\', r'\\')
        return "$" + new_expr + "$"
        
    # Also check if the expression contains exactly ` \sigma / \sqrt{n} ` as a substring
    # Since we are inside `$...$`, we can do targeted string replacements if it's safe.
    # But it's safer to just exact match the entire block.
    # Are there any math blocks with extra spaces?
    lookup_expr_stripped = lookup_expr.strip()
    if lookup_expr_stripped in exact_math_replacements:
        new_expr = exact_math_replacements[lookup_expr_stripped].replace('\\', r'\\')
        return "$ " + new_expr + " $" if expr.startswith(' ') else "$" + new_expr + "$"
        
    return m.group(0)

new_data = re.sub(r'\$(.*?)\$', replacer, data)

with codecs.open('data.js', 'w', 'utf-8') as f:
    f.write(new_data)

print("Replacement complete.")
