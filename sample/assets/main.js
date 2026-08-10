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

  // Lead form — POST to live API
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
        consent: form.consent && form.consent.checked,
        ts: new Date().toISOString()
      };

      var btn = form.querySelector('button[type="submit"]');
      var success = form.parentElement.querySelector('.form-success');
      var errorEl = form.parentElement.querySelector('.form-error');
      btn.disabled = true;
      btn.textContent = 'Enviando...';
      if (errorEl) errorEl.classList.remove('show');

      fetch('/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      .then(function(r) { return r.json().then(function(b) { return { ok: r.ok, body: b }; }); })
      .then(function(result) {
        if (result.ok && result.body.ok) {
          if (success) {
            success.classList.add('show');
            // Swap message based on priority
            var msg = success.querySelector('.success-msg');
            if (msg && result.body.priority === 'URGENT') {
              msg.textContent = 'Gracias. Atenderemos su consulta penal en menos de 30 minutos.';
            } else if (msg) {
              msg.textContent = 'Gracias. Un abogado de Rubicón EAS le enviará un mensaje en menos de 24 horas hábiles.';
            }
          }
          form.reset();
        } else {
          if (errorEl) {
            errorEl.textContent = 'Error: ' + (result.body.error || 'desconocido') +
              (result.body.fields ? ' (' + result.body.fields.join(', ') + ')' : '');
            errorEl.classList.add('show');
          }
        }
      })
      .catch(function(err) {
        if (errorEl) {
          errorEl.textContent = 'Error de red. Intente de nuevo o escriba directamente a nuestra línea.';
          errorEl.classList.add('show');
        }
      })
      .finally(function() {
        btn.disabled = false;
        btn.textContent = 'Enviar consulta';
      });
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
