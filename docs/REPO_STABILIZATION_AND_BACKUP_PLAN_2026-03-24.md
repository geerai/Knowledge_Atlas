# Repo Stabilization And Backup Plan

Date: 2026-03-24
Primary inventory:
- `/Users/davidusa/REPOS/Knowledge_Atlas/docs/REPO_INVENTORY_2026-03-24.md`

## Goal

Make active work fully recoverable and reduce repo ambiguity without doing destructive cleanup blindly.

## Governing rule

We do not start by deleting files or resetting repos.
We start by:
1. identifying authoritative repos
2. identifying accidental repo structures
3. separating safe-to-back-up work from local-only state
4. committing and pushing in focused streams

## Success conditions

The cleanup succeeds when:
1. each active project has one clear canonical repo
2. each canonical repo either has a remote or is explicitly marked local-only
3. no accidental parent repo is masking child project state
4. secrets and local machine state stay out of tracked commits
5. no important current work remains stranded only in a dirty worktree

## Phase A — Freeze and classify

Status:
- started

Actions:
1. inventory current repos and near-repos
2. classify each as:
   - canonical active repo
   - accidental repo
   - local-only corpus
   - legacy or auxiliary repo
3. note whether each has a valid remote and pushed branch

Current result:
- complete enough to start remediation

## Phase B — Repair structural repo problems first

Status:
- not executed yet

Priority 1:
- repair the accidental top-level git repo at `/Users/davidusa/REPOS`

Reason:
- it is currently making `Article_Finder_v3_2_3` look like part of a giant uncommitted parent repo
- until this is corrected, AF backup state is ambiguous

Important constraint:
- this step is destructive and requires explicit approval before acting

Likely action:
1. verify nothing important is intentionally tracked in `/Users/davidusa/REPOS/.git`
2. preserve any repo-level ignore patterns worth keeping
3. remove or archive the accidental root `.git`
4. re-check AF repo structure immediately afterward

Priority 2:
- normalize `Article_Finder_v3_2_3` into a real standalone repo with:
  - its own proper git root
  - its own remote
  - local-only secrets excluded

## Phase C — Stabilize canonical repos in dependency order

### 1. Knowledge_Atlas

Why first:
- GUI/home repo
- already has a good remote
- relatively bounded dirty state

Actions:
1. classify current dirty work into:
   - IA/docs
   - intake/AF integration
   - mode switch
   - tests/scripts
2. commit each stream cleanly
3. push after each commit set

### 2. Article_Eater_PostQuinean_v1_recovery

Why second:
- core extraction substrate
- currently the highest mixed-worktree risk among valid repos

Actions:
1. split tracked vs generated vs experimental artifacts
2. identify what must be backed up immediately
3. separate docs/spec work from data/run artifacts
4. commit by workstream, not by giant status dump

### 3. Designing_Experiments

Why third:
- important course/docs repo
- currently has no remote

Actions:
1. decide canonical remote destination
2. push after curating docs/scripts/frontend state
3. explicitly decide whether `frontend/` is legacy, retained, or mirrored into Knowledge_Atlas only

### 4. theory_guides

Why fourth:
- valuable but not yet operationally central

Actions:
1. decide whether it should remain standalone or be imported elsewhere
2. if standalone, initialize a real repo and remote

## Phase D — Protect local-only state

Apply everywhere:
1. verify secrets stay local-only
2. verify large generated artifacts are ignored unless intentionally canonical
3. ignore machine junk:
   - `.DS_Store`
   - `__pycache__/`
   - `*.db-wal`
   - `*.db-shm`
   - lockfiles and temp files
4. document any intentional exceptions

## Phase E — Add a workspace registry

Create one shared registry doc that states:
1. repo name
2. purpose
3. canonical status
4. remote URL
5. backup state
6. owner / main workflow

This is the long-term guard against drift.

## Execution order

1. confirm and repair accidental `/Users/davidusa/REPOS/.git`
2. normalize `Article_Finder_v3_2_3`
3. curate and push outstanding `Knowledge_Atlas` work
4. curate `Article_Eater_PostQuinean_v1_recovery`
5. create remote plan for `Designing_Experiments`
6. decide versioning strategy for `theory_guides`

## What can be done ballistically now

Without further approval:
1. finish inventory docs
2. classify dirty files
3. prepare commit batches
4. improve ignore patterns non-destructively
5. write the workspace registry

## What requires explicit approval

1. removing or archiving `/Users/davidusa/REPOS/.git`
2. any destructive deletion of local files
3. any large restructuring that could orphan current work
