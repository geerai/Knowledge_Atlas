(function() {
  const DEFAULT_MODE = 'student_explorer';

  function getStoredMode() {
    return sessionStorage.getItem('ka_active_mode')
      || localStorage.getItem('ka_user_type')
      || DEFAULT_MODE;
  }

  function setStoredMode(mode) {
    sessionStorage.setItem('ka_active_mode', mode);
    localStorage.setItem('ka_user_type', mode);

    const currentUserRaw = localStorage.getItem('ka_current_user');
    if (currentUserRaw) {
      try {
        const currentUser = JSON.parse(currentUserRaw);
        currentUser.userType = mode;
        if (!currentUser.navPreference) {
          currentUser.navPreference = inferNavPreference(mode);
        }
        localStorage.setItem('ka_current_user', JSON.stringify(currentUser));
      } catch (err) {
        // Keep mode persistence even if the demo user object is malformed.
      }
    }
  }

  function inferNavPreference(mode) {
    if (mode === 'contributor') return 'contribute_atlas';
    if (mode === 'theory_mechanism_explorer') return 'theory_mechanisms';
    if (mode === 'instructor') return 'build_test_experiments';
    return 'explore_literature';
  }

  function initModeControls(options) {
    const opts = options || {};
    const onApply = typeof opts.onApply === 'function' ? opts.onApply : function() {};
    const selectId = opts.selectId || null;
    const pillContainerId = opts.pillContainerId || null;
    const defaultMode = opts.defaultMode || DEFAULT_MODE;

    let activeMode = getStoredMode() || defaultMode;
    setStoredMode(activeMode);

    if (selectId) {
      const selectEl = document.getElementById(selectId);
      if (selectEl) {
        selectEl.value = activeMode;
        selectEl.addEventListener('change', function() {
          activeMode = this.value;
          setStoredMode(activeMode);
          syncControls(activeMode, selectId, pillContainerId);
          onApply(activeMode);
        });
      }
    }

    if (pillContainerId) {
      const pillContainer = document.getElementById(pillContainerId);
      if (pillContainer) {
        pillContainer.addEventListener('click', function(event) {
          const btn = event.target.closest('[data-ka-mode]');
          if (!btn) return;
          activeMode = btn.getAttribute('data-ka-mode');
          setStoredMode(activeMode);
          syncControls(activeMode, selectId, pillContainerId);
          onApply(activeMode);
        });
      }
    }

    syncControls(activeMode, selectId, pillContainerId);
    onApply(activeMode);
  }

  function syncControls(mode, selectId, pillContainerId) {
    if (selectId) {
      const selectEl = document.getElementById(selectId);
      if (selectEl) selectEl.value = mode;
    }
    if (pillContainerId) {
      const pillContainer = document.getElementById(pillContainerId);
      if (pillContainer) {
        pillContainer.querySelectorAll('[data-ka-mode]').forEach(function(btn) {
          btn.classList.toggle('active', btn.getAttribute('data-ka-mode') === mode);
        });
      }
    }
  }

  window.KA_MODE_SWITCH = {
    initModeControls: initModeControls,
    getStoredMode: getStoredMode,
    setStoredMode: setStoredMode
  };
})();
