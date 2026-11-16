/*
 * BRAIN colour theme switcher (light / dark / green).
 *
 * Loaded synchronously so the saved theme is applied before the page paints.
 * Any element with [data-theme-choice] inside a .theme-switcher becomes a
 * theme button; see assets/css/brain-themes.css for the palettes.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'brain-theme';
  var THEMES = ['light', 'dark', 'green'];
  var META_COLORS = { light: '#f5f9fa', dark: '#0d1a20', green: '#f4f8f2' };
  var root = document.documentElement;

  function readSaved() {
    try {
      return window.localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function save(theme) {
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {
      /* Private mode or blocked storage: the theme still applies for this page. */
    }
  }

  function syncControls(theme) {
    var buttons = document.querySelectorAll('[data-theme-choice]');
    for (var i = 0; i < buttons.length; i++) {
      var active = buttons[i].getAttribute('data-theme-choice') === theme;
      buttons[i].setAttribute('aria-checked', active ? 'true' : 'false');
      buttons[i].tabIndex = active ? 0 : -1;
    }
  }

  function apply(theme) {
    if (THEMES.indexOf(theme) === -1) theme = 'light';
    root.setAttribute('data-brain-theme', theme);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', META_COLORS[theme]);
    syncControls(theme);
    return theme;
  }

  function current() {
    return root.getAttribute('data-brain-theme') || 'light';
  }

  apply(readSaved());

  function choose(theme, focus) {
    save(apply(theme));
    if (focus) {
      var btn = document.querySelector('[data-theme-choice="' + theme + '"]');
      if (btn) btn.focus();
    }
  }

  function init() {
    syncControls(current());

    document.addEventListener('click', function (event) {
      var btn = event.target.closest && event.target.closest('[data-theme-choice]');
      if (btn) choose(btn.getAttribute('data-theme-choice'), false);
    });

    // Radio-group keyboard behaviour: arrows move between themes.
    document.addEventListener('keydown', function (event) {
      var btn = event.target.closest && event.target.closest('[data-theme-choice]');
      if (!btn) return;
      var step = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[event.key];
      if (!step) return;
      event.preventDefault();
      var idx = THEMES.indexOf(btn.getAttribute('data-theme-choice'));
      choose(THEMES[(idx + step + THEMES.length) % THEMES.length], true);
    });

    // Keep other open tabs in sync.
    window.addEventListener('storage', function (event) {
      if (event.key === STORAGE_KEY) apply(event.newValue);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
