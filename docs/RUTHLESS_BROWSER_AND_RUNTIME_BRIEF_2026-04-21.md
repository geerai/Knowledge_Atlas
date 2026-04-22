# Ruthless Browser And Runtime Brief

Date: 2026-04-21  
Target repo: `Knowledge_Atlas`  
Primary aim: catch the failures that previously slipped through because the shell loaded, the endpoint answered, but the actual user experience was still wrong.

## Rules

1. Do not reward partial success.
2. A page that loads with the wrong auth state is a failure.
3. A page that needs a manual hard refresh to become truthful is a failure.
4. A flow that returns `200` but shows the wrong DOM state is a failure.
5. Record exact URL, trigger, expected result, actual result, and whether the failure is browser-state, auth, payload, CSS/JS asset, or backend.

## Pre-Checks

Run these first:

```bash
python3 -m pytest tests/test_ka_canonical_navbar_session.py \
  tests/test_ka_user_type_session.py \
  tests/test_site_runtime_smoke.py \
  tests/test_ka_article_endpoints_fallback.py -q

node --check ka_canonical_navbar.js
node --check ka_user_type.js
python3 scripts/site_runtime_smoke.py --profile staging --repo-root .
```

If any of those fail, stop and repair before human browser review.

## Human Browser Attacks

Use a fresh private window first, then repeat selected checks in an ordinary cached window.

### 1. Anonymous shell truthfulness

Check:

- `/ka/ka_home.html`
- `/ka/ka_login.html`
- `/ka/ka_forgot_password.html`
- `/ka/ka_reset_password.html`
- `/ka/160sp/collect-articles-upload.html`

Expect:

- canonical navbar and shell present
- JS and CSS assets loaded
- anonymous nav shows `Log in` and `Register`
- no missing banner, missing favicon, or unstyled shell

### 2. Login state propagation without hard reload

Use a smoke student.

Procedure:

1. Open `ka_home.html`.
2. Open `ka_login.html` in the same tab and log in.
3. Confirm redirect succeeds.
4. Navigate back to the previously visited page.
5. Switch away and back to the tab.
6. Repeat once with browser back/forward.

Expect:

- signed-in navbar appears without manual hard refresh
- no lingering `Log in` / `Register`
- student/profile state appears correctly
- protected student elements can reappear when auth becomes true

Fail if:

- the page only becomes truthful after hard reload
- navbar and page body disagree about whether the user is signed in

### 3. A0 article intake state

Use a smoke student with a known assignment.

Check `/ka/160sp/collect-articles-upload.html`.

Expect:

- assigned question renders in the DOM
- Part 2 topic pool is populated
- no `404` from `/api/student/assignments`
- no empty-state lie where backend data exists but the page fails to show it

### 4. Reset and forgot-password flow

Use one address only once per attempt. Do not request multiple emails and then test an older link.

Expect:

- forgot-password page posts to the correct auth route
- email arrives
- newest link opens the reset page with canonical shell
- reset succeeds once
- reused link fails clearly and honestly

Fail if:

- the page claims auth `404` when the route is healthy
- the reset page renders outside the canonical shell
- the newest link is rejected while the token is still unused

### 5. Multi-tab consistency

Procedure:

1. Open two tabs on different KA pages.
2. Log in or log out in one tab.
3. Return to the other tab without reloading.

Expect:

- the second tab becomes truthful on focus or visibility return
- stale student/admin badges disappear when auth is gone
- stale anonymous controls disappear when auth is present

### 6. Admin surfaces

Using a safe admin token:

- class health
- roster
- grading
- any admin-specific navbar badge or menu state

Expect:

- protected surfaces are reachable only with the token/session intended
- no student page accidentally shows admin state

## Required Deliverable

Post findings under a section titled:

`### Ruthless browser/runtime review — 2026-04-21`

Use this format:

- `PASS`: exact flow and why it is now trustworthy
- `FAIL`: URL, trigger, expected, actual, likely layer, severity

## What This Brief Is For

This brief exists because the previous failures were not spectacular coding blunders. They were seam failures:

- shell versus browser cache
- token state versus session flags
- backend truth versus DOM truth
- successful email send versus usable reset page

Anything that merely proves the server is alive, while failing to prove the user sees the right thing, is insufficient.
