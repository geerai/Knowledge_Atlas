/*
 * ka_journey_nav.js
 *
 * Injects the left-hand journey sub-nav into any page that exposes
 *   <aside id="ka-journey-slot"></aside>
 * The current journey (determined by user role in localStorage
 * 'ka_current_user' or by body[data-ka-journey]) is rendered OPEN.
 * Sibling journeys are rendered CLOSED but visible, as escape hatches
 * per Nielsen's progressive-disclosure heuristic.
 *
 * Current-step highlighting is done by matching the step's href suffix
 * against location.pathname.
 *
 * Progress is read from localStorage keys:
 *   ka_journey_<journeyId>_completed   -> JSON array of completed hrefs
 *
 * Author: CW, 2026-04-15
 */
(function () {
  'use strict';

  function prefix() {
    return (location.pathname.indexOf('/160sp/') !== -1) ? '../' : '';
  }

  function readUser() {
    try {
      var raw = localStorage.getItem('ka_current_user');
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function currentJourneyId(journeys) {
    // 1. Explicit page-level override.
    var explicit = document.body.getAttribute('data-ka-journey');
    if (explicit) return explicit;
    // 2. User role mapping.
    var user = readUser() || {};
    var role = user.role || 'student';
    // Find first journey whose audience contains the role.
    for (var i = 0; i < journeys.length; i++) {
      var aud = journeys[i].audience || [];
      if (aud.indexOf(role) !== -1) return journeys[i].id;
    }
    // 3. Default.
    return journeys[0] ? journeys[0].id : '';
  }

  function readCompleted(journeyId) {
    try {
      var raw = localStorage.getItem('ka_journey_' + journeyId + '_completed');
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    } catch (e) { return []; }
  }

  function hrefMatchesHere(href) {
    if (!href) return false;
    // Last path segment of href.
    var hPath = href.replace(/^(\.\.\/)+/, '').replace(/[?#].*$/, '');
    var here  = location.pathname.replace(/[?#].*$/, '');
    return here.indexOf(hPath) !== -1;
  }

  function renderGroup(journey, isCurrent) {
    var pre = prefix();
    var completed = readCompleted(journey.id);
    var total = journey.steps.length;
    var done = 0;
    var stepsHtml = journey.steps.map(function (s) {
      var isHere = hrefMatchesHere(s.href);
      var isDone = completed.indexOf(s.href) !== -1;
      if (isDone) done += 1;
      var cls = isHere ? ' class="active"' : '';
      var mark = isDone ? ' ✓' : '';
      return '<a href="' + pre + s.href + '"' + cls + '>' + s.label + mark + '</a>';
    }).join('');
    var pct = total ? Math.round(100 * done / total) : 0;
    var progressHtml = '<div class="ka-journey-progress">Progress: ' + done + ' / ' + total +
      '<div class="bar"><span style="width:' + pct + '%"></span></div></div>';
    var openCls = isCurrent ? ' open' : '';
    var titleCls = isCurrent ? ' current' : '';
    return '<div class="ka-journey-group' + openCls + '" data-id="' + journey.id + '">' +
      '<div class="ka-journey-title' + titleCls + '">' +
        '<span>' + journey.label + '</span><span class="twisty">▸</span>' +
      '</div>' +
      '<div class="ka-journey-body">' + stepsHtml + progressHtml + '</div>' +
    '</div>';
  }

  function wireAccordion(root) {
    var groups = root.querySelectorAll('.ka-journey-group');
    groups.forEach(function (g) {
      var title = g.querySelector('.ka-journey-title');
      if (!title) return;
      title.addEventListener('click', function () { g.classList.toggle('open'); });
    });
  }

  function init() {
    var slot = document.getElementById('ka-journey-slot');
    if (!slot) return;
    fetch(prefix() + 'ka_journeys.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var journeys = (data && data.journeys) || [];
        var curId = currentJourneyId(journeys);
        var html = '<h4>Your Journeys</h4>' +
          journeys.map(function (j) { return renderGroup(j, j.id === curId); }).join('');
        slot.className = 'ka-journey-nav';
        slot.innerHTML = html;
        wireAccordion(slot);
      })
      .catch(function (e) {
        slot.innerHTML = '<p style="font-size:0.8rem;color:#8A9A96;">' +
          'Journeys unavailable.</p>';
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
