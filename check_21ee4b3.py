import subprocess
text = subprocess.check_output(['git', 'show', '21ee4b3:data.js']).decode('utf-8', errors='ignore')
print('21ee4b3 Unfixed E(X) = np is present:', 'text: "E(X) = np, V(X) = np^2"' in text)
print('21ee4b3 Unfixed P(A|B) is present:', 'text: "P(A ∪ B) / P(A)"' in text)
