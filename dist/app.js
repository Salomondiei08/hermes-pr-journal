
(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem('jay-theme');
  const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
  const setTheme = (mode) => {
    root.classList.toggle('light', mode === 'light');
    localStorage.setItem('jay-theme', mode);
  };
  setTheme(saved || (prefersLight ? 'light' : 'dark'));
  document.querySelectorAll('[data-theme-toggle]').forEach((btn) => btn.addEventListener('click', () => setTheme(root.classList.contains('light') ? 'dark' : 'light')));
  const grid = document.querySelector('[data-filterable-grid]');
  if (!grid) return;
  let activeStatus = 'all';
  let activeRepo = 'all';
  const cards = Array.from(grid.querySelectorAll('[data-status][data-repo]'));
  const rerender = () => cards.forEach((card) => {
    const statusOk = activeStatus === 'all' || card.dataset.status === activeStatus;
    const repoOk = activeRepo === 'all' || card.dataset.repo === activeRepo;
    card.classList.toggle('hidden', !(statusOk && repoOk));
  });
  document.querySelectorAll('[data-filter-status]').forEach((btn) => btn.addEventListener('click', () => {
    activeStatus = btn.dataset.filterStatus;
    document.querySelectorAll('[data-filter-status]').forEach((b) => b.classList.toggle('active', b === btn));
    rerender();
  }));
  document.querySelectorAll('[data-filter-repo]').forEach((btn) => btn.addEventListener('click', () => {
    activeRepo = btn.dataset.filterRepo;
    document.querySelectorAll('[data-filter-repo]').forEach((b) => b.classList.toggle('active', b === btn));
    rerender();
  }));
})();
