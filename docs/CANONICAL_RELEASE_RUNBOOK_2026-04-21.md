# Canonical release runbook — 2026-04-21

This is the short operational path for the live Knowledge Atlas site on `xrlab`.

It assumes:

- GitHub `master` is the release line
- staging checkout lives at `/home/dkirsh/ka-staging-2026-04-20`
- production tree lives at `/var/www/xrlab/ka`
- the runtime smoke suite is present in both trees

## What is verified

The runtime smoke suite checks:

- public page shells
- payload reachability
- auth health
- forgot-password
- local validator

When credentials are supplied, it can also check:

- student login
- `auth/me`
- assignments
- admin health
- admin roster
- admin grading

## Email status

As of 2026-04-21, the production forgot-password flow is restored:

- endpoint returns `registered: true`
- endpoint returns `email_sent: true`

That is the server-side criterion. Inbox delivery should still be checked occasionally by a human.

## Single canonical server command

Run this on `xrlab`:

```bash
cd /var/www/xrlab/ka
bash scripts/server_release_cycle.sh full
```

That does four things:

1. pulls the staging checkout to the latest `origin/master`
2. runs the staging runtime smoke suite
3. promotes the staging tree into production with safe exclusions and restores the production `data/` directory to the known working mode
4. runs the production runtime smoke suite

## Other useful modes

Only refresh staging and verify it:

```bash
cd /var/www/xrlab/ka
bash scripts/server_release_cycle.sh staging
```

Only promote staging into production:

```bash
cd /var/www/xrlab/ka
bash scripts/server_release_cycle.sh promote
```

Only run the production smoke suite:

```bash
cd /var/www/xrlab/ka
KA_SMOKE_RESET_EMAIL=dkirsh@ucsd.edu bash scripts/server_release_cycle.sh production-smoke
```

If `KA_SMOKE_RESET_EMAIL` is unset, the forgot-password check is skipped on purpose. This prevents an ordinary release run from invalidating a real user's live reset links.

## Important exclusions in promotion

Production promotion deliberately does **not** overwrite:

- `ka_config.js`
- `data/ka_auth.db`
- SQLite sidecar files
- `data/ka_auth_secret.txt`
- `.venv`
- historical smoke reports

That is intentional. The code and site assets are promoted; the live secrets and data are preserved.

## Expected outputs

Staging reports:

- `/home/dkirsh/ka-staging-2026-04-20/docs/runtime_smoke_reports/latest_staging.md`
- `/home/dkirsh/ka-staging-2026-04-20/docs/runtime_smoke_reports/latest_staging.json`

Production reports:

- `/var/www/xrlab/ka/docs/runtime_smoke_reports/latest_production.md`
- `/var/www/xrlab/ka/docs/runtime_smoke_reports/latest_production.json`

## When manual intervention is still needed

The script assumes the auth service is already healthy. If production forgot-password fails and the smoke report shows:

- connection refused, or
- bad gateway, or
- `email_sent: false`

then inspect:

- `systemctl status ka-auth.service`
- `/etc/ka-auth.env`
- directory permissions on `/var/www/xrlab/ka/data`

The known working data-directory mode is:

```bash
sudo chmod 2775 /var/www/xrlab/ka/data
sudo chgrp "domain users" /var/www/xrlab/ka/data
sudo /bin/systemctl restart ka-auth.service
```

The canonical release script now reapplies the `2775` mode and `domain users`
group during promotion, precisely to prevent the earlier forgot-password
regression from recurring.
