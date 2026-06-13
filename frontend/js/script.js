
/**
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
  }
});

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

document.addEventListener('DOMContentLoaded', () => {
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


const API_BASE_URL = window.APP_CONFIG.API_BASE_URL;

function getToken() {
  return localStorage.getItem("datarra_token");
}

function getStoredUser() {
  const rawUser = localStorage.getItem("datarra_user");
  return rawUser ? JSON.parse(rawUser) : null;
}

function saveUser(user) {
  localStorage.setItem("datarra_user", JSON.stringify(user));
}

function logout() {
  localStorage.removeItem("datarra_token");
  localStorage.removeItem("datarra_user");
  window.location.replace("login.html");
}

function requireAuth() {
  const token = getToken();

  if (!token) {
    window.location.href = "login.html";
  }
}

function requireAdmin() {
  requireAuth();

  const user = getStoredUser();

  if (!user || !user.is_admin) {
    window.location.href = "index.html";
  }
}

function setupAdminVisibility() {
  const user = getStoredUser();

  document.querySelectorAll("[data-admin-only]").forEach(el => {
    if (!user || !user.is_admin) {
      el.style.display = "none";
    }
  });
}

async function apiFetch(path, options = {}) {
  const token = getToken();

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  if (response.status === 401) {
    logout();
    return;
  }

  return response;
}


function getInitials(name) {
  return name
    .split(" ")
    .map(part => part[0] || "")
    .slice(0, 2)
    .join("")
    .toUpperCase();
}

function updateUserUI() {
  const user = getStoredUser();

  if (!user) return;

  const name = user.display_name || "User";
  const initials = getInitials(name);

  document.querySelectorAll("[data-user-name]").forEach(el => {
    el.textContent = name;
  });

  document.querySelectorAll("[data-user-initials]").forEach(el => {
    el.textContent = initials;
  });

  document.querySelectorAll("[data-user-role]").forEach(el => {
    el.textContent = user.is_admin ? "Admin" : "Data Explorer";
  });
}