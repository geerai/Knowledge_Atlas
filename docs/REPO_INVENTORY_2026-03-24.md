# Repo Inventory

Date: 2026-03-24
Scope: active repos and near-repos under `/Users/davidusa/REPOS`

## 1. Knowledge_Atlas

Path:
- `/Users/davidusa/REPOS/Knowledge_Atlas`

Role:
- canonical GUI / site repo

Git state:
- real git repo
- remote configured: `origin https://github.com/dkirsh/Knowledge_Atlas.git`
- `master` pushed and current through `e523629`
- track staging branches exist remotely:
  - `track/1-staging`
  - `track/2-staging`
  - `track/3-staging`
  - `track/4-staging`

Current dirty state:
- tracked modified files present
- substantial untracked doc/script/test layer present

Risk:
- medium

Primary issue:
- not structurally broken; just needs curated commits so current work is fully backed up

## 2. Article_Eater_PostQuinean_v1_recovery

Path:
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery`

Role:
- extraction / rebuild / JSON / summary substrate

Git state:
- real git repo
- remote configured: `origin https://github.com/dkirsh/Article_Eater.git`
- branch: `codex/recovery-cc-migration-artifacts`
- branch is ahead of remote

Current dirty state:
- very large tracked modified set
- extremely large untracked set
- data, docs, scripts, services, tests all mixed together

Risk:
- very high

Primary issue:
- this is the largest mixed worktree and cannot be made safe by a single blanket commit

## 3. Designing_Experiments

Path:
- `/Users/davidusa/REPOS/Designing_Experiments`

Role:
- course docs and experiment-design repo

Git state:
- real git repo
- no remote configured

Current dirty state:
- tracked modifications
- substantial untracked docs, tests, scripts, and `frontend/`

Risk:
- high

Primary issue:
- important content has no remote backup

## 4. Article_Finder_v3_2_3

Path:
- `/Users/davidusa/REPOS/Article_Finder_v3_2_3`

Role:
- article-finding/search/intake engine

Git state:
- structurally abnormal
- `git rev-parse --show-toplevel` resolves to `/Users/davidusa/REPOS`
- local `.git` directory only contains local exclude data
- no independent remote

Risk:
- critical

Primary issue:
- this is not behaving as an independent repo
- it is effectively inside an accidental parent git repo at `/Users/davidusa/REPOS`

## 5. REPOS root

Path:
- `/Users/davidusa/REPOS`

Role:
- should be a workspace directory, not a project repo

Git state:
- accidental top-level git repo
- no commits
- no remote
- enormous untracked tree including most child projects

Risk:
- critical

Primary issue:
- this accidental repo makes AF status misleading and creates backup ambiguity

## 6. theory_guides

Path:
- `/Users/davidusa/REPOS/theory_guides`

Role:
- theory-guide corpus

Git state:
- not a git repo
- no remote

Risk:
- medium to high depending on how actively it will be edited

Primary issue:
- valuable content exists with no versioned backup path

## Risk order

1. `/Users/davidusa/REPOS` accidental root git repo
2. `Article_Finder_v3_2_3`
3. `Article_Eater_PostQuinean_v1_recovery`
4. `Designing_Experiments`
5. `Knowledge_Atlas`
6. `theory_guides`
