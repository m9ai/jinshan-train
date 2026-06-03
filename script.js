// ===== 导航栏滚动 =====
const nav = document.getElementById('nav');
function onScroll() {
  if (window.scrollY > 40) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ===== 数字递增动画 =====
const numObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseInt(el.dataset.target, 10);
    if (isNaN(target)) return;
    let current = 0;
    const duration = 800;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.floor(current + (target - current) * e);
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = target;
    };
    requestAnimationFrame(tick);
    numObserver.unobserve(el);
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-target]').forEach(el => numObserver.observe(el));

// ===== 元素渐入动画 =====
const fadeObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      fadeObserver.unobserve(entry.target);
    }
  });
}, { rootMargin: '0px 0px -60px 0px', threshold: 0.1 });

document.querySelectorAll('.bento-card, .scenario-card, .cta-card, .compare-wrap, .station-track, .section-header, .showcase-text, .showcase-visual')
  .forEach(el => {
    el.classList.add('fade-up');
    fadeObserver.observe(el);
  });

// ===== 平滑滚动 =====
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    const y = target.getBoundingClientRect().top + window.pageYOffset - 80;
    window.scrollTo({ top: y, behavior: 'smooth' });
  });
});
