### CW commit 42d65fc — deployment

- Phase 1 result: PASS
  - `python3 scripts/gen_journey_pages.py` regenerated 15 journey pages with no committed drift.
  - Internal `href` targets in `ka_journey_*.html` resolved cleanly against the filesystem.
  - AF self-link suppression pattern was correct on `ka_journey_af_references.html`, `ka_journey_af_roi.html`, and `ka_journey_af_neuro.html`.
  - Claude's requested `python3 scripts/site_runtime_smoke.py --local` flag does not exist in the current script. Deviation: used the supported command `python3 scripts/site_runtime_smoke.py --profile staging --repo-root /Users/davidusa/REPOS/Knowledge_Atlas`, which passed with `28 pass, 0 fail, 0 skip`.

- Phase 2 result: PASS
  - `git push origin master` reported `Everything up-to-date`.

- Phase 3 Nginx fix: DONE
  - The staging alias had previously been serving HTML but 404ing `.js`, `.css`, and `.ico`.
  - Current staging asset checks now return `200` for `ka_canonical_navbar.js`, `ka_atlas_shell.css`, `ka_journey_page.css`, and `favicon.ico`.

- Phase 3 deploy result: PASS
  - Current staging path in use: `/home/dkirsh/ka-staging-2026-04-20`
  - Current deployment mechanism in use: `bash scripts/server_release_cycle.sh full`
  - Staging smoke at `2026-04-21T17:13:11Z` UTC: `28 pass, 0 fail, 0 skip`

- Phase 4 cut-over: PASS
  - Production path in use: `/var/www/xrlab/ka`
  - Deviation from Claude prompt: current production cut-over is handled by the canonical release script rather than an explicit `/srv/...` symlink flip.
  - Production refresh completed during the release cycle at `2026-04-21T17:13:14Z` UTC.
  - Production smoke at `2026-04-21T17:13:14Z` UTC: `22 pass, 0 fail, 6 skip`
  - Production favicon now returns `200`, and production forgot-password page now points at `/auth/forgot-password` rather than the stale `/api/auth/forgot-password` fallback.

- Any deviations from this prompt and why:
  - Deployed current `master` tip (`59ef0ad`) rather than checking out detached commit `42d65fc`, because `master` already contained `42d65fc` plus necessary hotfixes for staging assets, favicon delivery, and forgot-password routing.
  - Used the current server paths (`/home/dkirsh/ka-staging-2026-04-20` and `/var/www/xrlab/ka`) rather than the older `/srv/...` placeholders in the prompt.
  - The release script performs the production promotion atomically for this environment, so no manual symlink flip was required.

- Ping CW: deployment complete; staging and production are both green on the current master tip.
