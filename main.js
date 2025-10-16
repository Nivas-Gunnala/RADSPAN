(function ensureCanonical() {
  const existing = document.querySelector('link[rel="canonical"]');
  const href = location.origin + location.pathname;
  if (existing) existing.setAttribute('href', href);
  else {
    const link = document.createElement('link');
    link.setAttribute('rel', 'canonical');
    link.setAttribute('href', href);
    document.head.appendChild(link);
  }
})();

/* Header shadow on scroll */
(function headerShadow() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => {
    if (window.scrollY > 6) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

/* Mobile menu toggle */
(function mobileMenu() {
  const btn = document.getElementById('mobile-menu-toggle');
  const nav = document.getElementById('nav-links');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
})();

/* Simple toast */
function showToast(message, timeout = 2400) {
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = message;
  document.body.appendChild(el);
  requestAnimationFrame(() => el.classList.add('show'));
  setTimeout(() => {
    el.classList.remove('show');
    setTimeout(() => el.remove(), 250);
  }, timeout);
}

/* Contact form validation */
(function contactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(form);
    const name = (data.get('name') || '').toString().trim();
    const email = (data.get('email') || '').toString().trim();
    const message = (data.get('message') || '').toString().trim();

    if (!name || !email || !message) {
      showToast('Please fill in all fields.');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      showToast('Please enter a valid email.');
      return;
    }
    form.reset();
    showToast('Thanks! Your message has been sent.');
  });
})();

(function ensureCanonical() {
  const existing = document.querySelector('link[rel="canonical"]');
  const href = location.origin + location.pathname;
  if (existing) existing.setAttribute('href', href);
  else {
    const link = document.createElement('link');
    link.setAttribute('rel', 'canonical');
    link.setAttribute('href', href);
    document.head.appendChild(link);
  }
})();

/* Header shadow on scroll */
(function headerShadow() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const onScroll = () => {
    if (window.scrollY > 6) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

/* Mobile menu toggle */
(function mobileMenu() {
  const btn = document.getElementById('mobile-menu-toggle');
  const nav = document.getElementById('nav-links');
  if (!btn || !nav) return;
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
  });
})();
