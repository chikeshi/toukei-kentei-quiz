import codecs

with codecs.open('style.css', 'a', 'utf-8') as f:
    f.write("""
/* ----------------------------------
   Button: Previous
---------------------------------- */
.btn-prev {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  border-radius: var(--r-md);
  font-size: .95rem;
  font-weight: 700;
  letter-spacing: .02em;
  transition: background var(--t), transform var(--t), color var(--t), opacity var(--t);
  cursor: pointer;
}
.btn-prev:hover:not([disabled]) {
  background: var(--color-primary);
  color: #fff;
  transform: translateY(-2px);
}
.btn-prev[disabled] { opacity: .35; cursor: not-allowed; transform: none; }

/* ----------------------------------
   Result Details Accordion
---------------------------------- */
.result-details-section {
  margin-top: 32px;
}
.result-details-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.result-accordion {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--r-md);
  overflow: hidden;
}
.result-accordion[open] {
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.result-accordion-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  cursor: pointer;
  font-weight: 700;
  color: var(--color-text);
  background: var(--color-bg);
  transition: background var(--t);
  list-style: none; /* Hide default triangle */
}
.result-accordion-header::-webkit-details-marker {
  display: none; /* Hide for Safari */
}
.result-accordion-header:hover {
  background: rgba(0,0,0,0.02);
}
[data-theme="dark"] .result-accordion-header:hover {
  background: rgba(255,255,255,0.04);
}
.result-accordion-header .acc-icon {
  display: flex;
  align-items: center;
  gap: 12px;
}
.acc-verdict-icon {
  font-size: 1.2rem;
}
.acc-q-label {
  color: var(--color-primary);
}
.acc-cat-label {
  font-size: 0.85rem;
  color: var(--color-text-mut);
  font-weight: 400;
  margin-left: 8px;
}
.result-accordion-body {
  padding: 16px;
  border-top: 1px solid var(--color-border);
  font-size: 0.95rem;
  line-height: 1.6;
}
.acc-body-section {
  margin-bottom: 12px;
}
.acc-body-label {
  font-weight: 700;
  font-size: 0.85rem;
  color: var(--color-text-mut);
  margin-bottom: 4px;
}
.acc-body-content {
  color: var(--color-text);
}
.acc-body-content.user-wrong {
  color: var(--color-danger);
  font-weight: 600;
}
.acc-body-content.correct-ans {
  color: var(--color-success);
  font-weight: 600;
}
""")
