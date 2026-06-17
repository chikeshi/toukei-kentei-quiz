/* =====================================================
   統計検定2級 道場 – quiz.js
   ===================================================== */
'use strict';

// ============================================================
//  Category Definitions moved to data.js
// ============================================================

// ============================================================
//  選択中カテゴリ（Set で管理）
// ============================================================
const selectedCats = new Set(CATEGORIES.map(c => c.name)); // 初期：全選択

// ============================================================
//  Quiz Data  – 30問・各問に一意の id
// ============================================================

// ============================================================
//  State
// ============================================================
const state = {
  selectedCategories: [],
  questions:          [],
  currentIndex:       0,
  answered:           false,
  score:              { correct: 0, total: 0 },
  categoryResults:    {},
  currentQuestion:    null,
  answeredIds:        [],  // 解答した問題ID（順番通り）
  incorrectIds:       [],  // 不正解だった問題ID（フィルタリング等に活用可能）
  isRandom10:         false, // 10問抽出モードか
};

// ============================================================
//  Utility
// ============================================================
const $  = id => document.getElementById(id);

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function renderMath(el) {
  if (el && window.renderMathInElement) {
    renderMathInElement(el, {
      delimiters: [
        { left: '$$', right: '$$', display: true  },
        { left: '$',  right: '$',  display: false },
      ],
      throwOnError: false,
    });
  }
}

function countByCategory(catName) {
  return QUIZ_DATA.filter(q => q.category === catName).length;
}

// ============================================================
//  Screen Management
// ============================================================
function showScreen(screenId) {
  ['screenStart', 'screenQuiz', 'screenResult'].forEach(id => {
    const el = $(id);
    if (el) el.hidden = id !== screenId;
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================
//  START SCREEN
// ============================================================
function initStartScreen() {
  const grid = $('categoryGrid');
  grid.innerHTML = '';

  CATEGORIES.forEach(cat => {
    const count      = countByCategory(cat.name);
    const isSelected = selectedCats.has(cat.name);

    const card = document.createElement('div');
    card.className = 'category-card' + (isSelected ? ' is-checked' : '');
    card.dataset.cat = cat.name;
    card.setAttribute('role', 'checkbox');
    card.setAttribute('aria-checked', isSelected ? 'true' : 'false');
    card.setAttribute('tabindex', '0');

    card.innerHTML = `
      <div class="cat-card-top">
        <div class="cat-card-left">
          <span class="cat-icon">${cat.icon}</span>
          <span class="cat-name">${cat.name}</span>
        </div>
        <span class="cat-count">${count}問</span>
      </div>
      <div class="cat-desc">${cat.desc}</div>
      <div class="cat-checkmark">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
      </div>
    `;

    const toggle = () => {
      if (selectedCats.has(cat.name)) {
        selectedCats.delete(cat.name);
        card.classList.remove('is-checked');
        card.setAttribute('aria-checked', 'false');
      } else {
        selectedCats.add(cat.name);
        card.classList.add('is-checked');
        card.setAttribute('aria-checked', 'true');
      }
      updateStartSummary();
    };

    card.addEventListener('click', toggle);
    card.addEventListener('keydown', e => {
      if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); toggle(); }
    });

    grid.appendChild(card);
  });

  updateStartSummary();
}

function updateStartSummary() {
  const catCount = selectedCats.size;
  const totalQ   = [...selectedCats].reduce((sum, cat) => sum + countByCategory(cat), 0);

  $('summaryText').innerHTML = catCount > 0
    ? `<strong>${catCount}</strong> 分野 ／ <strong>${totalQ}</strong> 問 を選択中`
    : '分野が選択されていません';

  $('btnStart').disabled = catCount === 0;
  if ($('btnStart10')) $('btnStart10').disabled = catCount === 0;
}

// ============================================================
//  START QUIZ
// ============================================================
function startQuiz(isRandom10 = false) {
  state.selectedCategories = [...selectedCats];
  if (state.selectedCategories.length === 0) return;

  state.isRandom10 = isRandom10;

  const filtered    = QUIZ_DATA.filter(q => state.selectedCategories.includes(q.category));
  let shuffled      = shuffleArray(filtered);
  
  if (state.isRandom10 && shuffled.length > 10) {
    shuffled = shuffled.slice(0, 10);
  }
  state.questions = shuffled;

  state.currentIndex  = 0;
  state.answered      = false;
  state.score         = { correct: 0, total: 0 };
  state.categoryResults = {};
  state.answeredIds   = [];
  state.incorrectIds  = [];
  state.selectedCategories.forEach(c => { state.categoryResults[c] = { correct: 0, total: 0 }; });

  showScreen('screenQuiz');
  renderQuestion();
}

// ============================================================
//  RENDER QUESTION
// ============================================================
function renderQuestion() {
  const q = state.questions[state.currentIndex];
  state.currentQuestion = q;
  state.answered        = false;

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
  const shuffled = shuffleArray(q.answerOptions.map(o => ({ ...o })));
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

  // Feedback template – feedbackClickedRationale は選択肢個別の解説用
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
  btnNext.disabled = true;
  const isLast = state.currentIndex === state.questions.length - 1;
  btnNext.innerHTML = isLast
    ? `結果を見る <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>`
    : `次の問題へ <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`;

  const card = $('quizCard');
  card.style.animation = 'none';
  card.offsetHeight;
  card.style.animation = '';

  renderMath($('questionText'));
  renderMath(optCont);
}

// ============================================================
//  HANDLE ANSWER
// ============================================================
function handleAnswer(clickedBtn, clickedOpt, allOptions) {
  if (state.answered) return;
  state.answered = true;

  const isCorrect = clickedOpt.isCorrect;

  // スコア更新
  state.score.total++;
  if (isCorrect) state.score.correct++;

  // ID トラッキング（問題IDで管理）
  const q = state.currentQuestion;
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

    // クリックした選択肢（＝正解）の rationale を表示
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

    // クリックした（不正解）選択肢の rationale を薄赤ボックスで表示
    if (clickedRationale) {
      clickedRatEl.className = 'feedback-clicked-rationale fcr-wrong';
      clickedRatEl.innerHTML = `あなたが選んだ選択肢：${clickedRationale}`;
      clickedRatEl.hidden    = false;
    } else {
      clickedRatEl.hidden = true;
    }

    // 正解を示す
    if (correctOpt) {
      correctNote.hidden    = false;
      correctNote.innerHTML = `✓ 正解は「<strong>${correctOpt.text}</strong>」でした`;
    } else {
      correctNote.hidden = true;
    }

    // 正解の rationale を解説として表示
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
//  NEXT QUESTION
// ============================================================
function handleNext() {
  const isLast = state.currentIndex === state.questions.length - 1;
  if (isLast) {
    showResult();
  } else {
    state.currentIndex++;
    renderQuestion();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// ============================================================
//  RESULT SCREEN
// ============================================================
function showResult() {
  showScreen('screenResult');

  const { correct, total } = state.score;
  const pct = total > 0 ? Math.round((correct / total) * 100) : 0;

  $('resultCorrect').textContent = correct;
  $('resultTotal').textContent   = total;
  $('resultPct').textContent     = pct;

  let emoji, msg;
  if (pct >= 90)      { emoji = '🏆'; msg = '素晴らしい！ほぼ完璧です。本番でも自信を持って挑みましょう！'; }
  else if (pct >= 70) { emoji = '🎉'; msg = 'よくできました！苦手な分野を重点的に復習してみましょう。'; }
  else if (pct >= 50) { emoji = '📚'; msg = 'もう一息です！各問題の解説をじっくり読み直してみましょう。'; }
  else                { emoji = '💪'; msg = '基礎からしっかり学び直しましょう。繰り返し挑戦することが大切です！'; }

  $('resultEmoji').textContent   = emoji;
  $('resultMessage').textContent = msg;

  // カテゴリ別ブレイクダウン
  const breakdownList = $('breakdownList');
  breakdownList.innerHTML = '';
  const catInfo = {};
  CATEGORIES.forEach(c => { catInfo[c.name] = c.icon; });

  state.selectedCategories.forEach(cat => {
    const res    = state.categoryResults[cat] || { correct: 0, total: 0 };
    const catPct = res.total > 0 ? Math.round((res.correct / res.total) * 100) : 0;

    const item = document.createElement('div');
    item.className = 'breakdown-item';
    item.innerHTML = `
      <span class="bd-icon">${catInfo[cat] || '📌'}</span>
      <span class="bd-label">${cat}</span>
      <div class="bd-bar-wrap">
        <div class="bd-bar-fill" style="width:0%" data-pct="${catPct}"></div>
      </div>
      <span class="bd-score">${res.correct}/${res.total}</span>
    `;
    breakdownList.appendChild(item);
  });

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.querySelectorAll('.bd-bar-fill').forEach(bar => {
        bar.style.width = `${bar.dataset.pct}%`;
      });
    });
  });
}



// ============================================================
//  EVENT LISTENERS
// ============================================================
$('btnSelectAll').addEventListener('click', () => {
  CATEGORIES.forEach(c => selectedCats.add(c.name));
  document.querySelectorAll('#categoryGrid .category-card').forEach(card => {
    card.classList.add('is-checked');
    card.setAttribute('aria-checked', 'true');
  });
  updateStartSummary();
});

$('btnDeselectAll').addEventListener('click', () => {
  selectedCats.clear();
  document.querySelectorAll('#categoryGrid .category-card').forEach(card => {
    card.classList.remove('is-checked');
    card.setAttribute('aria-checked', 'false');
  });
  updateStartSummary();
});

$('btnStart').addEventListener('click', () => startQuiz(false));
if ($('btnStart10')) {
  $('btnStart10').addEventListener('click', () => startQuiz(true));
}

$('btnNext').addEventListener('click', handleNext);

const goHome = () => {
  if (confirm('ホーム画面に戻りますか？（現在の進捗はリセットされます）')) {
    showScreen('screenStart');
  }
};
$('btnBackToStart').addEventListener('click', goHome);
if ($('btnQuitToStart')) $('btnQuitToStart').addEventListener('click', goHome);

$('btnRetry').addEventListener('click', () => {
  const filtered = QUIZ_DATA.filter(q => state.selectedCategories.includes(q.category));
  let shuffled     = shuffleArray(filtered);
  if (state.isRandom10 && shuffled.length > 10) {
    shuffled = shuffled.slice(0, 10);
  }
  state.questions     = shuffled;
  state.currentIndex  = 0;
  state.answered      = false;
  state.score         = { correct: 0, total: 0 };
  state.answeredIds   = [];
  state.incorrectIds  = [];
  state.selectedCategories.forEach(c => { state.categoryResults[c] = { correct: 0, total: 0 }; });
  showScreen('screenQuiz');
  renderQuestion();
});

$('btnGoStart').addEventListener('click', () => showScreen('screenStart'));



// ============================================================
//  BOOTSTRAP
// ============================================================
let _bootstrapped = false;
function bootstrap() {
  if (_bootstrapped) return;
  _bootstrapped = true;
  initStartScreen();
  showScreen('screenStart');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', bootstrap);
} else {
  bootstrap();
}
