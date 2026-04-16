
(function () {
  'use strict';

  /* ── Constants ── */
  const API = window.__KA_CONFIG__?.apiBase ?? '';
  const token = localStorage.getItem('ka_access_token');

  /* ── DOM handles ── */
  const form       = document.querySelector('#signup form');
  const nameInput  = document.getElementById('name');
  const emailInput = document.getElementById('email');
  const trackSel   = document.getElementById('track');
  const reasonTxt  = document.getElementById('reason');
  const submitBtn  = form.querySelector('button[type="submit"]');
  const callout    = document.querySelector('#signup .callout');
  const signupNote = form.querySelector('.signup-note');

  const TRACK_NAMES = {
    track1: 'Track 1: Image Tagger',
    track2: 'Track 2: Article Finder',
    track3: 'Track 3: VR Production',
    track4: 'Track 4: GUI Evaluation'
  };

  /* ── Helpers ── */
  function showMessage(type, text) {
    let box = document.getElementById('signup-message');
    if (!box) {
      box = document.createElement('div');
      box.id = 'signup-message';
      box.style.cssText = 'border-radius:8px; padding:1rem 1.2rem; margin:1rem 0; font-size:0.9rem;';
      form.parentNode.insertBefore(box, form.nextSibling);
    }
    if (type === 'success') {
      box.style.background = '#d4edda';
      box.style.borderLeft = '4px solid var(--teal)';
      box.style.color = '#155724';
    } else {
      box.style.background = '#f8d7da';
      box.style.borderLeft = '4px solid #c0392b';
      box.style.color = '#721c24';
    }
    box.innerHTML = text;
    box.style.display = '';
  }

  function enableForm() {
    [nameInput, emailInput, trackSel, reasonTxt, submitBtn].forEach(el => {
      el.disabled = false;
    });
  }

  function disableForm() {
    [nameInput, emailInput, trackSel, reasonTxt, submitBtn].forEach(el => {
      el.disabled = true;
    });
  }

  /* ── Not logged in: update callout, leave form disabled ── */
  if (!token) {
    callout.innerHTML =
      '<div class="callout-label">Login Required</div>' +
      '<p>You must <a href="../ka_login.html" style="color:var(--teal);font-weight:600;">log in</a> ' +
      'to sign up for a track. If you don\'t have an account yet, ' +
      '<a href="../ka_login.html" style="color:var(--teal);font-weight:600;">register first</a>.</p>';
    return;
  }

  /* ── Logged in: fetch profile, pre-fill form, enable it ── */
  fetch(API + '/auth/me', {
    headers: { 'Authorization': 'Bearer ' + token }
  })
  .then(function (res) {
    if (!res.ok) throw new Error('Auth failed (' + res.status + ')');
    return res.json();
  })
  .then(function (user) {
    /* Pre-fill name and email from profile (read-only) */
    var fullName = ((user.first_name || '') + ' ' + (user.last_name || '')).trim();
    nameInput.value  = fullName;
    emailInput.value = user.email || '';
    nameInput.readOnly  = true;
    emailInput.readOnly = true;

    /* If user already has a track, show it and allow change */
    if (user.track && TRACK_NAMES[user.track]) {
      callout.innerHTML =
        '<div class="callout-label">Current Track</div>' +
        '<p>You are currently signed up for <strong>' + TRACK_NAMES[user.track] + '</strong>. ' +
        'You can change your track until the end of Week 3.</p>';
      trackSel.value = user.track;
      signupNote.textContent = 'Submitting will update your track selection.';
    } else {
      callout.innerHTML =
        '<div class="callout-label">Ready to Sign Up</div>' +
        '<p>You are logged in as <strong>' + (fullName || user.email) + '</strong>. ' +
        'Select a track below and submit your choice.</p>';
      signupNote.textContent = 'You can change your track until the end of Week 3.';
    }

    enableForm();
    /* Keep name/email visually enabled but not editable */
    nameInput.style.background  = '#f0f0f0';
    emailInput.style.background = '#f0f0f0';
  })
  .catch(function (err) {
    console.warn('[KA Track Signup] Auth check failed:', err);
    callout.innerHTML =
      '<div class="callout-label">Connection Issue</div>' +
      '<p>Could not verify your login. Please make sure you are ' +
      '<a href="../ka_login.html" style="color:var(--teal);font-weight:600;">logged in</a> ' +
      'and try again. If the problem persists, the auth server may be unavailable.</p>';
  });

  /* ── Form submission ── */
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var selectedTrack = trackSel.value;
    if (!selectedTrack) {
      showMessage('error', '<strong>Please select a track</strong> before submitting.');
      return;
    }

    /* Disable while submitting */
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting…';

    fetch(API + '/auth/update-track', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ track: selectedTrack })
    })
    .then(function (res) {
      if (!res.ok) return res.json().then(function (d) { throw new Error(d.detail || 'Server error'); });
      return res.json();
    })
    .then(function (data) {
      showMessage('success',
        '<strong>Track confirmed!</strong> ' + data.message +
        '<br><span style="font-size:0.85rem;color:#555;">You can change your selection until the end of Week 3.</span>');

      /* Update callout to reflect new selection */
      callout.innerHTML =
        '<div class="callout-label">Current Track</div>' +
        '<p>You are signed up for <strong>' + (data.track_name || TRACK_NAMES[selectedTrack]) + '</strong>. ' +
        'You can change your track until the end of Week 3.</p>';

      submitBtn.textContent = 'Update Track';
      submitBtn.disabled = false;
      signupNote.textContent = 'Submitting will update your track selection.';
    })
    .catch(function (err) {
      showMessage('error',
        '<strong>Signup failed.</strong> ' + (err.message || 'Please try again.') +
        '<br><span style="font-size:0.85rem;">If this persists, contact the instructor.</span>');
      submitBtn.textContent = 'Submit Signup';
      submitBtn.disabled = false;
    });
  });
})();
