(function() {
  function getCurrentUser() {
    try {
      return JSON.parse(localStorage.getItem('ka_current_user') || 'null');
    } catch (_err) {
      return null;
    }
  }

  function initialsFor(user, fallback) {
    if (!user) return fallback || 'KA';
    const first = (user.firstName || user.name || '').trim();
    const last = (user.lastName || '').trim();
    const initials = `${first[0] || ''}${last[0] || ''}`.toUpperCase();
    return initials || fallback || 'KA';
  }

  function fullNameFor(user, fallback) {
    if (!user) return fallback || '';
    const parts = [user.firstName, user.lastName].filter(Boolean);
    return parts.join(' ').trim() || user.name || fallback || '';
  }

  function applyUser(options) {
    const opts = options || {};
    const user = getCurrentUser();

    if (opts.avatarId) {
      const avatar = document.getElementById(opts.avatarId);
      if (avatar) avatar.textContent = initialsFor(user, opts.avatarFallback);
    }

    if (opts.nameId) {
      const nameEl = document.getElementById(opts.nameId);
      if (nameEl) nameEl.textContent = fullNameFor(user, opts.nameFallback);
    }

    if (opts.emailId) {
      const emailEl = document.getElementById(opts.emailId);
      if (emailEl) emailEl.textContent = user && user.email ? user.email : (opts.emailFallback || '');
    }
  }

  window.KA_SHELL_USER = {
    applyUser: applyUser,
    getCurrentUser: getCurrentUser
  };
})();
