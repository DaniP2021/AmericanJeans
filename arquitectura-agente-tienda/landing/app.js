/* American Jeans — landing Fase 1
   JS mínimo: año del footer, medición de clics a WhatsApp y de apertura de FAQ.
   Sin dependencias. Si GA4 no está cargado, no rompe: los eventos se ignoran. */

(function () {
  'use strict';

  var anio = document.getElementById('anio');
  if (anio) anio.textContent = String(new Date().getFullYear());

  function enviar(evento, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', evento, params);
    } else if (Array.isArray(window.dataLayer)) {
      window.dataLayer.push(Object.assign({ event: evento }, params));
    }
  }

  /* Clics a WhatsApp: se miden por sección de origen para saber qué mensaje convierte. */
  document.querySelectorAll('[data-wa]').forEach(function (el) {
    el.addEventListener('click', function () {
      enviar('whatsapp_click', {
        seccion: el.getAttribute('data-wa'),
        ubicacion: 'landing_fase1'
      });
    });
  });

  /* Apertura de preguntas: mide qué duda frena la compra. */
  document.querySelectorAll('.faq__item').forEach(function (item) {
    item.addEventListener('toggle', function () {
      if (!item.open) return;
      var pregunta = item.querySelector('summary');
      enviar('faq_open', {
        pregunta: pregunta ? pregunta.textContent.trim() : 'sin_titulo'
      });
    });
  });

  /* Si el usuario ya probó la guía de talles, marcamos la intención. */
  var talles = document.getElementById('talles-link');
  if (talles) {
    talles.addEventListener('click', function () {
      enviar('talles_open', { ubicacion: 'landing_fase1' });
    });
  }

  /* El menú móvil es un <details>: al elegir una sección se cierra solo. */
  var menu = document.querySelector('.menu');
  if (menu) {
    menu.querySelectorAll('.menu__panel a').forEach(function (link) {
      link.addEventListener('click', function () {
        menu.open = false;
        enviar('menu_click', { seccion: link.getAttribute('href') });
      });
    });
    document.addEventListener('click', function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.open) {
        menu.open = false;
        var btn = menu.querySelector('.menu__btn');
        if (btn) btn.focus();
      }
    });
  }
})();
