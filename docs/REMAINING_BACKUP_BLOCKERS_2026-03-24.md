# Remaining Backup Blockers

Date: 2026-03-24

## Completed in this cleanup pass

- archived the accidental workspace-level git metadata from `/Users/davidusa/REPOS/.git` into `/Users/davidusa/REPOS/Backups/REPOS_root_git_backup_2026-03-24`
- restored independent repo behavior for:
  - `/Users/davidusa/REPOS/Knowledge_Atlas`
  - `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery`
  - `/Users/davidusa/REPOS/Designing_Experiments`
  - `/Users/davidusa/REPOS/Article_Finder_v3_2_3`
- pushed `Knowledge_Atlas/master` through commit `f7af13d`
- pushed `Article_Eater_PostQuinean_v1_recovery/codex/recovery-cc-migration-artifacts` through commit `31f0d2d87`
- moved a substantial set of loose root docs into canonical repo-local `docs/` directories
- embedded the Master Doc maintenance rule directly into the canonical Master Doc
- wrote the workspace registry and relocation audit

## Remaining blockers

### 1. `Designing_Experiments` has no remote
Path:
- `/Users/davidusa/REPOS/Designing_Experiments`

Current state:
- real git repo
- local commit history exists
- no GitHub remote configured

Consequence:
- local history exists, but there is no off-machine backup for that repo

Required next action:
- create a GitHub repo and add `origin`
- then push the current branches

### 2. `Article_Finder_v3_2_3` has no remote and no curated initial snapshot
Path:
- `/Users/davidusa/REPOS/Article_Finder_v3_2_3`

Current state:
- restored as a standalone local git repo after the root repo archive
- no remote configured
- no curated commit boundary yet

Consequence:
- the repo is structurally fixed, but still not backed up remotely

Required next action:
- decide the canonical remote repo name
- add minimal ignore rules if needed
- make the first curated commit
- push it

### 3. `theory_guides` is still not versioned as its own repo
Path:
- `/Users/davidusa/REPOS/theory_guides`

Current state:
- active content corpus
- no git repo
- no remote

Consequence:
- the guide corpus still depends entirely on the local filesystem

Required next action:
- decide whether to:
  - keep it as an auxiliary content directory and absorb it elsewhere
  - or make it a real repo with its own remote

### 4. A few root-level duplicates and workspace-operational files remain
Examples:
- `/Users/davidusa/REPOS/MASTER_DOC_CMR_2026-02-25.md`
- `/Users/davidusa/REPOS/TOPIC_PROGRESS.md`
- `/Users/davidusa/REPOS/EXPERIMENT_WIZARD_README.md`
- `/Users/davidusa/REPOS/ENGINEERING_PANEL_AND_SPRINT_PLAN_2026-03-10.md`
- `/Users/davidusa/REPOS/LAYER_REVISION_PANEL_DELIBERATION_2026-03-10.md`

Consequence:
- the root is much cleaner, but not fully normalized yet

Required next action:
- decide which of these should remain workflow-level exceptions and which should be retired or archived

## Source-of-truth status after this pass

### Canonical and remotely backed up
- `Knowledge_Atlas`
- `Article_Eater_PostQuinean_v1_recovery`

### Canonical but still local-only
- `Designing_Experiments`
- `Article_Finder_v3_2_3`
- `theory_guides`

## Bottom line

The workspace is no longer structurally confused.
The remaining work is repo provisioning and final normalization, not emergency cleanup.
