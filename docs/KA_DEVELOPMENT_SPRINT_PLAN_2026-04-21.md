# Knowledge Atlas Development Sprint Plan

Date: 2026-04-21  
Status: Active  
Inputs: local code inspection, production/staging incidents from 2026-04-20 to 2026-04-21, panel consultation from `Socrates` and `Anscombe`

## Purpose

The site is now usable, but it is not yet orderly enough. The failures we have just seen were not random. They came from three structural weaknesses:

1. client auth/session state is fragmented across local storage, session storage, and page-specific assumptions;
2. the release gate is stronger than before, but still too thin at the browser-behaviour layer;
3. content quality on the public site still lags the stronger V7 science-summary, PNU, and theory state.

The programme below orders the work so that reliability comes before ornament.

## Panel Synthesis

### Socrates

Recommended order:

1. auth/session unification
2. browser-level testing
3. admin and reset-link hardening
4. release hardening
5. soft content rebuild
6. product and UX work

Reason: identity coherence is the first precondition; only then do browser tests and release discipline become trustworthy.

### Anscombe

Recommended concerns:

1. semantic freeze on the ontology and crosswalks
2. classifier and extractability contract alignment
3. operational repair before public elaboration

Reason: the site should not outrun the semantic system that supports it.

### Decision

Use Socrates' ordering for execution. Carry Anscombe's semantic concerns into the later rebuild and product sprints so the public site does not drift away from the content contracts.

## Sprint Structure

### Sprint 1 — Auth And Browser-State Coherence

Goal:
Make login, logout, page restore, tab changes, and back/forward cache restores converge on one truthful client auth state.

Scope:

- make `ka_canonical_navbar.js` and `ka_user_type.js` re-read auth state on `pageshow`, `focus`, `visibilitychange`, `storage`, and an explicit custom auth-change event;
- hydrate legacy session keys from canonical local auth state;
- clear stale gated/admin session flags when no valid local auth remains;
- make gated elements reappear correctly when auth state changes rather than remaining hidden forever;
- make real login/logout surfaces notify the rest of the shell about auth changes.

Acceptance criteria:

- a student who logs in and returns to a previously open page sees the signed-in navbar without a manual hard refresh;
- a stale session-only student/admin state no longer survives after logout;
- protected DOM sections can hide and unhide correctly on refresh.

Status:
In progress on 2026-04-21.

### Sprint 2 — Ruthless Browser Validation

Goal:
Catch user-visible failures that HTTP-only smoke cannot see.

Scope:

- add browser-driven checks for login, navbar/profile state, A0 assigned-question rendering, Q2 topic pool rendering, forgot-password shell, and reset-password shell;
- make the ruthless browser brief part of the pre-production gate;
- keep the checks server-runnable where practical.

Acceptance criteria:

- a browser test fails if login succeeds but the navbar still shows `Log in` / `Register`;
- a browser test fails if A0 loads but the assigned question or Q2 pool is missing in the DOM;
- a browser test fails if reset and forgot-password pages render without the canonical shell.

### Sprint 3 — Admin And Reset Reliability

Goal:
Stop treating protected checks as optional omissions.

Scope:

- provide a safe admin-smoke token path for staging and production;
- make production forgot-password smoke opt-in but explicit;
- pin down the reset-link handling edge cases and document the one-valid-link rule clearly in the UI and runbook.

Acceptance criteria:

- admin health, roster, and grading checks are green in the ordinary staging gate;
- production can run the protected checks safely from `.smoke.env`;
- reset-link failures are distinguishable as backend, link, or user-flow errors.

### Sprint 4 — Release And Service Hardening

Goal:
Reduce manual operational fragility.

Scope:

- make the release script verify the auth service version it is actually serving;
- make the service restart step narrow and reliable;
- make staging and production release evidence easier to compare.

Acceptance criteria:

- after deploy, the served auth health and frontend assets prove they match the checked-out tree;
- the release runbook no longer depends on memory of past incidents.

### Sprint 5 — Soft Research Rebuild

Goal:
Improve public payload quality without pretending that strict gold is complete.

Scope:

- rebuild public payloads from the improved science summaries, PNUs, theories, and crosswalk surfaces;
- surface those gains in article, theory, mechanism, and topic pages;
- keep the distinction between soft rebuild and strict gold rebuild explicit.

Acceptance criteria:

- the public payloads reflect the newer research state materially better than the current bundle;
- the rebuild is documented as soft, not falsely canonical.

### Sprint 6 — Product And Journey Work

Goal:
Turn the now-stable shell into a more coherent intellectual tool.

Scope:

- strengthen article pages with summaries, contradictions/support lists, theory and mechanism links, and better section navigation;
- improve journey pages and role-specific flows;
- surface the GUI-track showcase pages intentionally rather than as hidden curiosities.

Acceptance criteria:

- the article and journey surfaces visibly benefit from the rebuilt content;
- role-based flows feel coherent instead of accreted.

## Near-Term Execution Order

The immediate sequence is:

1. finish Sprint 1 code and tests;
2. write and run a ruthless browser/runtime brief for Sprint 1;
3. start Sprint 2 with the most valuable browser checks;
4. then return to admin/reset and release hardening.

## Notes

- This plan does not claim the whole programme can be completed in one turn.
- It is meant to prevent the common vice of doing six half-fixes at once and calling it a strategy.
