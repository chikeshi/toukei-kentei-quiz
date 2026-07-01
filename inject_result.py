import codecs

with codecs.open('quiz.js', 'r', 'utf-8') as f:
    js = f.read()

show_result_addition = """
  // 詳細結果（アコーディオンリスト）の生成
  const detailsList = $('resultDetailsList');
  if (detailsList) {
    detailsList.innerHTML = '';
    state.questions.forEach((q, idx) => {
      // ユーザーの回答を取得
      const userOpt = q.userOpt;
      if (!userOpt) return; // 未解答のものはスキップ
      
      const isCorrect = userOpt.isCorrect;
      const correctOpt = q.answerOptions.find(o => o.isCorrect) || {};
      
      const detailsEl = document.createElement('details');
      detailsEl.className = 'result-accordion';
      
      detailsEl.innerHTML = `
        <summary class="result-accordion-header">
          <div class="acc-icon">
            <span class="acc-verdict-icon">${isCorrect ? '🟢' : '❌'}</span>
            <span class="acc-q-label">Q${idx + 1}</span>
            <span class="acc-cat-label">${q.category}</span>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="acc-chevron"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </summary>
        <div class="result-accordion-body">
          <div class="acc-body-section">
            <div class="acc-body-label">問題</div>
            <div class="acc-body-content">${q.question}</div>
          </div>
          <div class="acc-body-section">
            <div class="acc-body-label">あなたの回答</div>
            <div class="acc-body-content ${isCorrect ? 'correct-ans' : 'user-wrong'}">${userOpt.text}</div>
          </div>
          ${!isCorrect ? `
          <div class="acc-body-section">
            <div class="acc-body-label">正解</div>
            <div class="acc-body-content correct-ans">${correctOpt.text}</div>
          </div>
          ` : ''}
          <div class="acc-body-section">
            <div class="acc-body-label">解説</div>
            <div class="acc-body-content">${correctOpt.rationale || userOpt.rationale || ''}</div>
          </div>
        </div>
      `;
      detailsList.appendChild(detailsEl);
    });
    
    // アコーディオンを開いた時に数式レンダリングを実行
    detailsList.querySelectorAll('.result-accordion').forEach(acc => {
      acc.addEventListener('toggle', (e) => {
        if (acc.open) {
          renderMath(acc);
        }
      });
    });
  }
"""

marker = "breakdownList.appendChild(item);\n  });"
if marker in js:
    js = js.replace(marker, marker + "\n" + show_result_addition)
    with codecs.open('quiz.js', 'w', 'utf-8') as f:
        f.write(js)
    print("Injected showResult logic!")
else:
    print("Marker not found!")
