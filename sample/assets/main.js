// Rubicón EAS — Sample Website JavaScript
// Vanilla JS, no dependencies. Handles: FAQ accordion, mobile nav, lead form.

(function() {
  'use strict';

  // Mobile nav toggle
  var navToggle = document.querySelector('.nav-toggle');
  var navMenu = document.querySelector('nav ul');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function() {
      navMenu.classList.toggle('open');
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-item q').forEach(function(q) {
    q.addEventListener('click', function() {
      var item = q.parentElement;
      var wasOpen = item.classList.contains('open');
      // Close siblings within same section
      item.parentElement.querySelectorAll('.faq-item.open').forEach(function(i) {
        i.classList.remove('open');
      });
      if (!wasOpen) item.classList.add('open');
    });
  });

  // Lead form
  var form = document.querySelector('.form form');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var data = {
        name: form.name && form.name.value,
        phone: form.phone && form.phone.value,
        email: form.email && form.email.value,
        area: form.area && form.area.value,
        summary: form.summary && form.summary.value,
        ts: new Date().toISOString()
      };

      // In production: POST to /api/lead which forwards to n8n webhook → Evolution API
      console.log('Lead payload:', data);

      // Optimistic UI
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = 'Enviando...';

      // Simulate latency
      setTimeout(function() {
        var success = form.parentElement.querySelector('.form-success');
        if (success) {
          success.classList.add('show');
          form.reset();
        }
        btn.disabled = false;
        btn.textContent = 'Enviar consulta';
      }, 800);
    });
  }

  // Smooth scroll for hash links
  document.querySelectorAll('a[href^="#"]').forEach(function(a) {
    a.addEventListener('click', function(e) {
      var hash = a.getAttribute('href');
      if (hash.length > 1) {
        var target = document.querySelector(hash);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });
})();
