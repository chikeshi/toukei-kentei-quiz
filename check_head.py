import subprocess
text = subprocess.check_output(['git', 'show', 'HEAD:data.js']).decode('utf-8', errors='ignore')
print('Unfixed E(X) = np is present:', 'text: "E(X) = np, V(X) = np^2"' in text)
print('Unfixed P(A|B) is present:', 'text: "P(A ∪ B) / P(A)"' in text)
