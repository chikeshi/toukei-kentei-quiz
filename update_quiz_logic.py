import codecs
import re

with codecs.open('quiz.js', 'r', 'utf-8') as f:
    js = f.read()

# 1. Update renderQuestion to handle q.isAnswered
render_question_replacement = """function renderQuestion() {
  const q = state.questions[state.currentIndex];
  state.currentQuestion = q;
  state.answered        = q.isAnswered || false;

  $('questionBadge').textContent = `Q${state.currentIndex + 1}`;
  $('categoryBadge').textContent = q.category;
  if ($('idBadge')) $('idBadge').textContent = `ID: ${q.id}`;

  const pct = Math.round((state.currentIndex / state.questions.length) * 100);
  $('progressBar').style.width    = `${pct}%`;
  $('progressLabel').textContent  = `問題 ${state.currentIndex + 1} / ${state.questions.length}`;
  $('progressPct').textContent    = `${pct}%`;

  $('hdrScoreCorrect').textContent = state.score.correct;
  $('hdrScoreTotal').textContent   = state.score.total;

  $('questionText').innerHTML = q.question;

  // Build shuffled options
  let shuffled;
  if (q.isAnswered && q.shuffledOptions) {
    shuffled = q.shuffledOptions;
  } else {
    shuffled = shuffleArray(q.answerOptions.map(o => ({ ...o })));
    q.shuffledOptions = shuffled;
  }
  
  const optCont  = $('optionsContainer');
  optCont.innerHTML = '';
  const LABELS = ['A', 'B', 'C', 'D'];

  shuffled.forEach((opt, idx) => {
    const btn = document.createElement('button');
    btn.className         = 'option-btn';
    btn.dataset.isCorrect = opt.isCorrect ? '1' : '0';
    btn.id                = `opt-${idx}`;
    btn.innerHTML = `
      <span class="opt-label">${LABELS[idx]}</span>
      <span class="opt-text">${opt.text}</span>
    `;
    btn.addEventListener('click', () => handleAnswer(btn, opt, shuffled));
    optCont.appendChild(btn);
  });

  // Feedback template
  const fb = $('feedbackArea');
  fb.classList.remove('open');
  fb.innerHTML = `
    <div id="feedbackInner" class="feedback-inner">
      <div id="feedbackVerdict"         class="feedback-verdict"></div>
      <div id="feedbackClickedRationale" class="feedback-clicked-rationale" hidden></div>
      <div id="feedbackCorrectNote"     class="feedback-correct-note"      hidden></div>
      <div id="feedbackSectionLabel"    class="feedback-section-label"     hidden>解説</div>
      <div id="feedbackRationale"       class="feedback-rationale"         hidden></div>
    </div>
  `;

  const btnNext = $('btnNext');
  const isLast = state.currentIndex === state.questions.length - 1;
  btnNext.disabled = !q.isAnswered;
  btnNext.innerHTML = isLast
    ? `結果を見る <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`
    : `次の問題へ <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`;

  const btnPrev = $('btnPrev');
  if (btnPrev) {
    if (state.currentIndex === 0) {
      btnPrev.disabled = true;
      btnPrev.style.visibility = 'hidden';
    } else {
      btnPrev.disabled = false;
      btnPrev.style.visibility = 'visible';
    }
  }

  const card = $('quizCard');
  card.style.animation = 'none';
  card.offsetHeight;
  card.style.animation = '';

  renderMath($('questionText'));
  renderMath(optCont);

  if (q.isAnswered) {
    // Restore visual feedback silently (without incrementing score)
    restoreFeedbackState(q, shuffled);
  }
}

function restoreFeedbackState(q, allOptions) {
  const isCorrect = q.userOpt.isCorrect;
  const btns = $('optionsContainer').querySelectorAll('.option-btn');
  
  btns.forEach(btn => {
    btn.disabled = true;
    const isCorrectBtn = btn.dataset.isCorrect === '1';
    
    // Check if this button was the one clicked
    const isClickedBtn = (btn.id === q.clickedBtnId);
    
    if (isClickedBtn) {
      btn.classList.add(isCorrect ? 'correct' : 'wrong');
      const icon = document.createElement('span');
      icon.className   = 'opt-result-icon';
      icon.textContent = isCorrect ? '✓' : '✗';
      btn.appendChild(icon);
    } else if (isCorrectBtn && !isCorrect) {
      btn.classList.add('correct');
      const icon = document.createElement('span');
      icon.className   = 'opt-result-icon';
      icon.textContent = '✓';
      btn.appendChild(icon);
    }
  });

  const fbInner         = $('feedbackInner');
  const verdict         = $('feedbackVerdict');
  const clickedRatEl    = $('feedbackClickedRationale');
  const correctNote     = $('feedbackCorrectNote');
  const sectionLabel    = $('feedbackSectionLabel');
  const rationaleEl     = $('feedbackRationale');

  const clickedRationale = q.userOpt.rationale || null;
  const correctOpt       = allOptions.find(o => o.isCorrect);
  const correctRationale = correctOpt?.rationale  || null;

  fbInner.className = `feedback-inner ${isCorrect ? 'fb-correct' : 'fb-wrong'}`;

  if (isCorrect) {
    verdict.className = 'feedback-verdict verdict-correct';
    verdict.innerHTML = '<span>🟢</span><span>正解！</span>';
    if (clickedRationale) {
      clickedRatEl.className = 'feedback-clicked-rationale fcr-correct';
      clickedRatEl.innerHTML = clickedRationale;
      clickedRatEl.hidden    = false;
    } else {
      clickedRatEl.hidden = true;
    }
    correctNote.hidden  = true;
    sectionLabel.hidden = true;
    rationaleEl.hidden  = true;
  } else {
    verdict.className = 'feedback-verdict verdict-wrong';
    verdict.innerHTML = '<span>❌</span><span>不正解…</span>';
    if (clickedRationale) {
      clickedRatEl.className = 'feedback-clicked-rationale fcr-wrong';
      clickedRatEl.innerHTML = `あなたが選んだ選択肢：${clickedRationale}`;
      clickedRatEl.hidden    = false;
    } else {
      clickedRatEl.hidden = true;
    }
    if (correctOpt) {
      correctNote.hidden    = false;
      correctNote.innerHTML = `✓ 正解は「<strong>${correctOpt.text}</strong>」でした`;
    } else {
      correctNote.hidden = true;
    }
    if (correctRationale) {
      sectionLabel.hidden   = false;
      rationaleEl.hidden    = false;
      rationaleEl.innerHTML = correctRationale;
    } else {
      sectionLabel.hidden = true;
      rationaleEl.hidden  = true;
    }
  }

  $('feedbackArea').classList.add('open');
  renderMath($('feedbackArea'));
}"""

js = re.sub(r'function renderQuestion\(\)\s*\{.*?(?=\n// ===|\nfunction handleAnswer)', render_question_replacement + '\n', js, flags=re.DOTALL)

# 2. Update handleAnswer
handle_answer_replacement = """function handleAnswer(clickedBtn, clickedOpt, allOptions) {
  if (state.answered) return;
  state.answered = true;

  const isCorrect = clickedOpt.isCorrect;

  // Record user's choice to the question state
  const q = state.currentQuestion;
  q.isAnswered = true;
  q.userOpt = clickedOpt;
  q.clickedBtnId = clickedBtn.id;

  // スコア更新
  state.score.total++;
  if (isCorrect) state.score.correct++;

  // ID トラッキング（問題IDで管理）
  state.answeredIds.push(q.id);
  if (!isCorrect) state.incorrectIds.push(q.id);

  // カテゴリ別スコア
  const cat = q.category;
  if (state.categoryResults[cat]) {
    state.categoryResults[cat].total++;
    if (isCorrect) state.categoryResults[cat].correct++;
  }

  // ヘッダースコア更新
  $('hdrScoreCorrect').textContent = state.score.correct;
  $('hdrScoreTotal').textContent   = state.score.total;

  // 選択肢ボタンのスタイル変更
  const btns = $('optionsContainer').querySelectorAll('.option-btn');
  btns.forEach(btn => {
    btn.disabled = true;
    const isCorrectBtn = btn.dataset.isCorrect === '1';
    if (btn === clickedBtn) {
      btn.classList.add(isCorrect ? 'correct' : 'wrong');
      const icon = document.createElement('span');
      icon.className   = 'opt-result-icon';
      icon.textContent = isCorrect ? '✓' : '✗';
      btn.appendChild(icon);
    } else if (isCorrectBtn && !isCorrect) {
      btn.classList.add('correct');
      const icon = document.createElement('span');
      icon.className   = 'opt-result-icon';
      icon.textContent = '✓';
      btn.appendChild(icon);
    }
  });

  // フィードバック要素取得
  const fbInner         = $('feedbackInner');
  const verdict         = $('feedbackVerdict');
  const clickedRatEl    = $('feedbackClickedRationale');
  const correctNote     = $('feedbackCorrectNote');
  const sectionLabel    = $('feedbackSectionLabel');
  const rationaleEl     = $('feedbackRationale');

  // 各選択肢の rationale
  const clickedRationale = clickedOpt.rationale  || null;
  const correctOpt       = allOptions.find(o => o.isCorrect);
  const correctRationale = correctOpt?.rationale  || null;

  fbInner.className = `feedback-inner ${isCorrect ? 'fb-correct' : 'fb-wrong'}`;

  if (isCorrect) {
    /* ── 正解 ─────────────────────────────────── */
    verdict.className = 'feedback-verdict verdict-correct';
    verdict.innerHTML = '<span>🟢</span><span>正解！</span>';

    if (clickedRationale) {
      clickedRatEl.className = 'feedback-clicked-rationale fcr-correct';
      clickedRatEl.innerHTML = clickedRationale;
      clickedRatEl.hidden    = false;
    } else {
      clickedRatEl.hidden = true;
    }

    correctNote.hidden  = true;
    sectionLabel.hidden = true;
    rationaleEl.hidden  = true;

  } else {
    /* ── 不正解 ───────────────────────────────── */
    verdict.className = 'feedback-verdict verdict-wrong';
    verdict.innerHTML = '<span>❌</span><span>不正解…</span>';

    if (clickedRationale) {
      clickedRatEl.className = 'feedback-clicked-rationale fcr-wrong';
      clickedRatEl.innerHTML = `あなたが選んだ選択肢：${clickedRationale}`;
      clickedRatEl.hidden    = false;
    } else {
      clickedRatEl.hidden = true;
    }

    if (correctOpt) {
      correctNote.hidden    = false;
      correctNote.innerHTML = `✓ 正解は「<strong>${correctOpt.text}</strong>」でした`;
    } else {
      correctNote.hidden = true;
    }

    if (correctRationale) {
      sectionLabel.hidden   = false;
      rationaleEl.hidden    = false;
      rationaleEl.innerHTML = correctRationale;
    } else {
      sectionLabel.hidden = true;
      rationaleEl.hidden  = true;
    }
  }

  // フィードバックアニメーション
  requestAnimationFrame(() => {
    $('feedbackArea').classList.add('open');
  });

  setTimeout(() => {
    renderMath($('feedbackArea'));
    $('feedbackArea').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, 80);

  $('btnNext').disabled = false;
}

// ============================================================
//  PREV QUESTION
// ============================================================
function handlePrev() {
  if (state.currentIndex > 0) {
    state.currentIndex--;
    renderQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
"""

js = re.sub(r'function handleAnswer\(clickedBtn, clickedOpt, allOptions\)\s*\{.*?(?=\n// ===|\nfunction handleNext)', handle_answer_replacement + '\n', js, flags=re.DOTALL)


# 3. Modify showResult to render accordion
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

js = re.sub(r'(breakdownList\.appendChild\(item\);\s*\});', r'\1' + '\n' + show_result_addition, js, flags=re.DOTALL)


with codecs.open('quiz_updated.js', 'w', 'utf-8') as f:
    f.write(js)
