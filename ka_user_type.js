/* ────────────────────────────────────────────────────────────────
   ka_user_type.js — shared access-control companion for K-ATLAS
   Include on every page:   <script src="ka_user_type.js" defer></script>

   Model
   -----
   Public user types (anyone, no login):
     visitor, researcher, practitioner, contributor
   Gated user types (login required):
     160-student, instructor

   Admin override
   --------------
   When ka.admin === 'yes' and ka.impersonating === 'true', the admin is
   silently viewing the site as another user type. A persistent amber banner
   at the top of every page confirms the impersonation and offers one-click
   return-to-admin or stop-impersonating.

   Per-element gating
   ------------------
   Mark any element that only enrolled students should see:
     <div data-ka-requires="160-student"> … </div>
   The element is hidden from unauthenticated visitors but remains visible
   for admins impersonating 160 Student (or for the student themselves).

   Replace storage (sessionStorage) with a server-backed session cookie in
   production. See ka_admin.html → ADMIN_API for the corresponding seam.
   ──────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  var PUBLIC_TYPES = ['visitor', 'researcher', 'practitioner', 'contributor'];
  var GATED_TYPES  = ['160-student', 'instructor'];

  var SS = window.sessionStorage;
  var LS = window.localStorage;
  function g(k) { try { return SS.getItem(k); } catch (e) { return null; } }
  function s(k, v) { try { SS.setItem(k, v); } catch (e) {} }
  function rm(k) { try { SS.removeItem(k); } catch (e) {} }
  function lg(k) { try { return LS.getItem(k); } catch (e) { return null; } }

  var KA = window.KA = window.KA || {};

  function readCurrentUser() {
    try {
      var raw = lg('ka_current_user');
      return raw ? JSON.parse(raw) : null;
    } catch (e) {
      return null;
    }
  }

  function hasAccessToken() {
    return !!lg('ka_access_token');
  }

  function syncCompatSessionFromLocalAuth() {
    var user = readCurrentUser();
    var authed = hasAccessToken() && user && user.email;
    if (!authed) {
      rm('ka.admin');
      rm('ka.adminEmail');
      rm('ka.adminRole');
      rm('ka.impersonating');
      rm('ka.160.authed');
      rm('ka.studentEmail');
      if (GATED_TYPES.indexOf(g('ka.userType')) >= 0) s('ka.userType', 'visitor');
      return null;
    }

    var role = String(user.role || '').toLowerCase();
    if (role === 'instructor' || role === 'admin') {
      s('ka.admin', 'yes');
      s('ka.adminEmail', user.email);
      s('ka.adminRole', role);
      rm('ka.160.authed');
      rm('ka.studentEmail');
      if (!g('ka.userType')) s('ka.userType', 'instructor');
      return user;
    }

    s('ka.160.authed', 'yes');
    s('ka.studentEmail', user.email);
    rm('ka.admin');
    rm('ka.adminEmail');
    rm('ka.adminRole');
    if (!g('ka.userType') || g('ka.userType') === 'visitor') s('ka.userType', '160-student');
    return user;
  }

  KA.userType = {
    /** Which user type is the viewer currently acting as? */
    get: function () {
      syncCompatSessionFromLocalAuth();
      return g('ka.userType') || 'visitor';
    },

    /** Set the viewer's user type. Pass {impersonate:true} for admin override. */
    set: function (type, opts) {
      opts = opts || {};
      s('ka.userType', type);
      if (opts.impersonate) s('ka.impersonating', 'true');
      else rm('ka.impersonating');
      if (opts.reload !== false) location.reload();
    },

    isPublic: function (t) { return PUBLIC_TYPES.indexOf(t) >= 0; },
    isGated:  function (t) { return GATED_TYPES.indexOf(t)  >= 0; },
    isAdmin:  function ()  { return g('ka.admin') === 'yes'; },
    isImpersonating: function () { return g('ka.impersonating') === 'true'; },

    /**
     * May the current viewer see content marked for `type`?
     *  - public types: always yes
     *  - gated types: yes if the viewer authenticated for that type,
     *                 or if an admin is impersonating that type.
     */
    canSee: function (type) {
      if (!type || PUBLIC_TYPES.indexOf(type) >= 0) return true;
      if (KA.userType.isAdmin()) return true;
      if (type === '160-student') return g('ka.160.authed') === 'yes';
      if (type === 'instructor')  return g('ka.admin') === 'yes';
      return false;
    },

    stopImpersonating: function () {
      rm('ka.impersonating');
      s('ka.userType', 'instructor');
      location.reload();
    }
  };

  /* ─── Impersonation banner ─── */
  function mountBanner() {
    if (!KA.userType.isAdmin() || !KA.userType.isImpersonating()) return;
    var ut = KA.userType.get();
    var bar = document.createElement('div');
    bar.id = 'ka-imp-banner';
    bar.setAttribute('role', 'status');
    bar.style.cssText =
      'position:fixed;top:0;left:0;right:0;z-index:9999;' +
      'background:#E8872A;color:#fff;padding:6px 16px;text-align:center;' +
      'font:600 0.82rem -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;' +
      'box-shadow:0 2px 6px rgba(0,0,0,0.2);';
    bar.innerHTML =
      'Viewing as <b>' + esc(ut) + '</b> &middot; ' +
      '<a href="160sp/ka_admin.html" style="color:#fff;text-decoration:underline;">Return to admin</a> &middot; ' +
      '<a href="#" id="ka-imp-stop" style="color:#fff;text-decoration:underline;">Stop impersonating</a>';
    document.body.insertBefore(bar, document.body.firstChild);
    if (!document.body.dataset.kaImpBasePaddingTop) {
      document.body.dataset.kaImpBasePaddingTop = String(parseInt(getComputedStyle(document.body).paddingTop, 10) || 0);
    }
    document.body.style.paddingTop =
      (parseInt(document.body.dataset.kaImpBasePaddingTop, 10) + 32) + 'px';
    var stop = document.getElementById('ka-imp-stop');
    if (stop) stop.addEventListener('click', function (e) {
      e.preventDefault();
      KA.userType.stopImpersonating();
    });
  }

  /* ─── Per-element gating ─── */
  function applyElementGates() {
    var els = document.querySelectorAll('[data-ka-requires]');
    for (var i = 0; i < els.length; i++) {
      var need = els[i].getAttribute('data-ka-requires');
      if (!KA.userType.canSee(need)) {
        els[i].style.display = 'none';
        els[i].setAttribute('data-ka-gated', 'hidden');
      } else {
        els[i].removeAttribute('data-ka-gated');
        els[i].style.removeProperty('display');
      }
    }
  }

  function removeBanner() {
    var bar = document.getElementById('ka-imp-banner');
    if (bar && bar.parentNode) bar.parentNode.removeChild(bar);
    if (document.body && document.body.dataset.kaImpBasePaddingTop) {
      document.body.style.paddingTop = document.body.dataset.kaImpBasePaddingTop + 'px';
      delete document.body.dataset.kaImpBasePaddingTop;
    }
  }

  function refreshState() {
    syncCompatSessionFromLocalAuth();
    removeBanner();
    mountBanner();
    applyElementGates();
  }

  function bindRefreshHooks() {
    if (KA.userType._refreshHooksBound) return;
    function maybeRefresh(ev) {
      if (!ev || !ev.key ||
          ev.key === 'ka_access_token' ||
          ev.key === 'ka_current_user' ||
          ev.key === 'ka_logged_in' ||
          ev.key === 'ka.userType' ||
          ev.key === 'ka.admin' ||
          ev.key === 'ka.160.authed') {
        refreshState();
      }
    }
    if (typeof window.addEventListener === 'function') {
      window.addEventListener('pageshow', refreshState);
      window.addEventListener('focus', refreshState);
      window.addEventListener('storage', maybeRefresh);
      window.addEventListener('ka-auth-state-changed', refreshState);
    }
    if (typeof document.addEventListener === 'function') {
      document.addEventListener('visibilitychange', function () {
        if (document.visibilityState === 'visible') refreshState();
      });
    }
    KA.userType._refreshHooksBound = true;
  }

  /* ─── Helpers ─── */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' })[c];
    });
  }

  /* ─── Boot (after DOM) ─── */
  KA.userType.refresh = refreshState;
  bindRefreshHooks();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      refreshState();
    });
  } else {
    refreshState();
  }
})();
