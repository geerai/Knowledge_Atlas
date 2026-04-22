# Ruthless Prompt — Site Validation

Date: 2026-04-22  
Target repo: `Knowledge_Atlas`  
Purpose: force a reviewer to test the site as a user would encounter it, not as a server would flatter it.

## Instruction

You are reviewing the live Knowledge Atlas site after a deploy.

You must be ruthless in a disciplined way.

Do not confuse:

- `200 OK` with correctness
- a live backend with a truthful page
- a working login endpoint with a page that visibly knows the user is logged in
- a reset email being sent with a reset page that behaves honestly

Any place where the browser and the backend disagree is a defect.

## Rules

1. Do not credit partial success.
2. A page that only becomes truthful after manual hard reload is a failure.
3. A protected page that loads but shows stale anonymous state is a failure.
4. A reset flow that returns `200` but misleads the user is a failure.
5. Record exact URL, trigger, expected result, actual result, likely layer, and severity.

## Pre-flight

Run these first in the repo root:

```bash
python3 -m pytest \
  tests/test_browser_runtime_smoke.py \
  tests/test_a0_api_base_contract.py \
  tests/test_ka_canonical_navbar_session.py \
  tests/test_ka_user_type_session.py \
  tests/test_site_runtime_smoke.py \
  tests/test_ka_article_endpoints_fallback.py -q

node --check ka_canonical_navbar.js
node --check ka_user_type.js
python3 scripts/site_validator.py
```

If those fail, stop and repair before claiming anything about the live site.

## Automated server checks

Run the HTTP/runtime suite:

```bash
bash scripts/run_site_runtime_smoke.sh staging
bash scripts/run_site_runtime_smoke.sh production
```

If you are explicitly testing forgot-password in browser mode, set the reset
email only for the environment you mean to exercise:

```bash
KA_BROWSER_SMOKE_STAGING_RESET_EMAIL=jpark@ucsd.edu \
  bash scripts/run_browser_runtime_smoke.sh staging

bash scripts/run_browser_runtime_smoke.sh production
```

The production browser run should normally omit a reset email so you do not
invalidate a live link without reason.

## Required browser attacks

### 1. Anonymous shell truth

Open, without prior login:

- `/ka/ka_home.html`
- `/ka/ka_forgot_password.html`
- `/ka/ka_reset_password.html?token=invalid-browser-smoke-token`
- `/ka/160sp/collect-articles-upload.html`
- `/ka/160sp/ka_admin.html`

Expect:

- canonical navbar present
- correct CSS and JS assets loaded
- anonymous navbar shows `Log in` and `Register`
- A0 shows the login overlay
- admin page shows the instructor sign-in gate
- reset page rejects the invalid token clearly, inside the normal shell

### 2. Cross-tab login truth

With a smoke student:

1. open `ka_home.html`
2. open `ka_user_home.html`
3. open `160sp/collect-articles-upload.html`
4. log in through `ka_login.html`
5. return to the already open tabs without manual hard refresh

Expect:

- home navbar becomes signed-in
- user-home top bar becomes signed-in
- A0 shows the assigned Question 1 and the Question 2 topic pool

Fail if any tab remains stale until forced reload.

### 3. Cross-tab logout truth

From the signed-in state:

1. log out using the canonical navbar
2. revisit the already open pages

Expect:

- home returns to anonymous controls
- user-home returns to anonymous top-bar state
- A0 restores the login overlay and clears visible assignment state

### 4. Forgot-password truth

If a reset email is explicitly configured for the environment:

1. submit the forgot-password form
2. inspect the page message

Expect:

- not a network-error lie
- not a false `404` claim
- a success or manual-reset message that matches backend reality

### 5. Protected admin/runtime truth

If admin token and safe credentials are available:

- admin class health
- roster
- grading

Expect:

- protected checks are green in runtime smoke
- no anonymous or student page leaks admin data

## Deliverable format

Post findings under:

`### Ruthless site validation — 2026-04-22`

Use:

- `PASS`: exact flow and why it is trustworthy
- `FAIL`: URL, trigger, expected, actual, likely layer, severity

## What counts as success

Success is not “the site mostly works.”

Success is:

- runtime smoke green except for intentional protected skips
- browser smoke green for the stated flow set
- no stale auth state across tabs
- no A0 assignment lie
- no dishonest reset-token handling
- no admin shell pretending to be public
