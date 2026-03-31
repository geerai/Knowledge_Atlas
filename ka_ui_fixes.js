/**
 * ka_ui_fixes.js
 * Knowledge Atlas — UI fixes for floating buttons and About section
 *
 * Loaded after ka_about_page.js and ka_page_function.js.
 * 1. Hides the About This Page section by default (show on click toggle)
 * 2. Right-aligns both floating buttons (ABOUT THIS PAGE + PAGE FUNCTION)
 * 3. Removes PAGE FUNCTION button if it duplicates About content
 */
(function () {
  'use strict';

  window.addEventListener('load', function () {
    /* ── 1. Hide "About This Page" section by default ── */
    var sec = document.getElementById('about-this-page');
    if (sec) {
      sec.style.display = 'none';
    }

    /* ── 2. Make About trigger toggle visibility ── */
    var trigger = document.getElementById('ka-about-trigger');
    if (trigger && sec) {
      // Remove old listeners by cloning
      var newTrigger = trigger.cloneNode(true);
      trigger.parentNode.replaceChild(newTrigger, trigger);
      newTrigger.addEventListener('click', function (e) {
        e.preventDefault();
        if (sec.style.display === 'none') {
          sec.style.display = 'block';
          sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
          sec.style.display = 'none';
        }
      });
    }

    /* ── 3. Right-align both floating buttons ── */
    var fnBtn = document.getElementById('ka-fn-btn');
    var aboutBtn = document.getElementById('ka-about-trigger') || newTrigger;

    if (aboutBtn) {
      aboutBtn.style.right = '24px';
      aboutBtn.style.bottom = '52px';
    }
    if (fnBtn) {
      fnBtn.style.right = '24px';
      fnBtn.style.bottom = '18px';
    }
  });
})();
