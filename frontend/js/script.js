/**
 * DataBerry — Shared JavaScript
 * Global utilities used across all pages
 */

// ── Counter animation ────────────────────────────────────
/**
 * Animate a number element from 0 to target.
 * @param {HTMLElement} el
 * @param {number} target
 * @param {number} duration  ms
 */
function animateCounter(el, target, duration = 1000) {
  if (!el) return;
  const start = performance.now();
  const easeOut = t => 1 - Math.pow(1 - t, 3);

  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const value = Math.round(easeOut(progress) * target);
    el.textContent = value.toLocaleString();
    if (progress < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// ── Keyboard shortcuts (global) ──────────────────────────
document.addEventListener('keydown', (e) => {
  const meta = e.metaKey || e.ctrlKey;
  if (!meta) return;

  switch (e.key) {
    case 'n':
      e.preventDefault();
      window.location.href = 'analysis.html';
      break;
    case 'h':
      e.preventDefault();
      window.location.href = 'history.html';
      break;
    // Add more shortcuts here as needed
  }
});

// ── Scroll reveal ────────────────────────────────────────
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.card, .stat-card, .history-card').forEach(el => {
    observer.observe(el);
  });
}

function isAdminAuthenticated() {
  return sessionStorage.getItem('adminAuthenticated') === 'true';
}

function authenticateAdmin(username, password) {
  const validUser = 'admin';
  const validPass = 'password123';
  if (username === validUser && password === validPass) {
    sessionStorage.setItem('adminAuthenticated', 'true');
    return true;
  }
  return false;
}

function requireAdminAuth() {
  if (!isAdminAuthenticated()) {
    window.location.replace('login.html');
  }
}

function logoutAdmin() {
  sessionStorage.removeItem('adminAuthenticated');
  window.location.replace('login.html');
}

// ── Init on DOM ready ────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Mark the current nav link as active based on URL
  const path = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href === path || (path === '' && href === 'index.html')) {
      link.classList.add('active');
    } else if (href !== '#') {
      link.classList.remove('active');
    }
  });
});
