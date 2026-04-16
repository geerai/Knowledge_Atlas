# Mode Switch Component Spec

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Audience: CW and GUI implementers
Purpose: define the anonymous and logged-in user-type mode switch so users get an immediate visible payoff when selecting a user type

## Why this component matters

If users choose a user type and nothing visible changes, the choice feels fake.

The system should therefore give an immediate reward:
- the navbar changes
- featured entry points change
- the user understands that the site is adapting to them

This is the point of the mode switch.

## Core behavior

When a user selects a mode:
1. the navbar reorders immediately
2. the highlighted primary lane changes
3. featured cards or calls to action reorder
4. a small explanation confirms what changed

Example:
- `Mode: Researcher`
- `Showing evidence, gaps, article tools, theory, and neural routes first`

## Scope

This component should work:
- before login
- after login
- across main KA pages

It should be:
- lightweight
- reversible
- persistent

## User types

Recommended user types:
- `student_explorer`
- `researcher`
- `contributor`
- `instructor`
- `practitioner`
- `theory_mechanism_explorer`

## Visible labels

Use clear labels:
- `Student Explorer`
- `Researcher`
- `Contributor`
- `Instructor`
- `Practitioner`
- `Theory + Mechanisms`

Avoid overly academic labels in the selector itself.

## Placement

### Before login

Place a visible lightweight selector:
- on `ka_home.html`
- optionally on `ka_topics.html`
- optionally in the top nav on key public pages

Recommended forms:
- segmented control
- mode pill with dropdown
- compact card row on home

### After login

Keep a small persistent control in the navbar:
- `Mode: Student Explorer`
- with a `Switch` affordance

## What changes by mode

### 1. Navbar order

The top-level emphasis should reorder.

### 2. Primary CTA

The main button should change.

### 3. Secondary entry cards

The first row of cards on home or section pages should reorder.

### 4. Explore dropdown contents

Under `Explore the Literature`, the top items should reorder by mode.

## What must not change

1. the underlying information architecture
2. the existence of other lanes
3. provenance and uncertainty treatment
4. the warm KA visual language

This is adaptive emphasis, not a different product per user.

## Per-mode behavior

### Student Explorer

Promote:
- Topics
- Evidence
- Gaps
- Course / Studio
- Build an Experiment

Primary CTA:
- `Explore Topics`

### Researcher

Promote:
- Evidence
- Gaps
- Article Search
- Theory Guides
- Neural Underpinnings

Primary CTA:
- `Search the Literature`

### Contributor

Promote:
- Dashboard
- Articles
- Tagging
- Approval
- Contributor assignments

Primary CTA:
- `Open Dashboard`

### Instructor

Promote:
- Course / Studio
- Dashboard
- Approval
- Assignments
- Article-finder and GUI-track resources

Primary CTA:
- `Open Course Tools`

### Practitioner

Promote:
- Topics
- Evidence
- Article summaries
- practical gaps
- theory only as secondary support

Primary CTA:
- `Browse Practical Topics`

### Theory + Mechanisms

Promote:
- Theory Guides
- Neural Underpinnings
- Evidence
- Topics
- Gaps

Primary CTA:
- `Open Theory Guides`

## Storage model

### Anonymous

Store:
- `ka_user_type`
- `ka_nav_preference`
- `ka_mode_source = anonymous`

### Logged-in

Store in `ka_current_user`:
- `userType`
- `navPreference`

And optionally mirror to:
- `ka_user_type`
- `ka_nav_preference`

## Precedence

Resolve active mode in this order:
1. explicit mode chosen this session
2. logged-in account preference
3. saved anonymous preference
4. default public mode

## Feedback behavior

After the user changes mode:
- animate the active mode pill
- update nav order
- update CTA text
- show a small transient confirmation

Do not use a modal for this.

## Minimal implementation contract

CW can implement this incrementally.

### Phase 1

1. mode selector on `ka_home.html`
2. localStorage persistence
3. navbar reorder on:
- `ka_home.html`
- `ka_topics.html`
- `ka_evidence.html`
- `ka_dashboard.html`

### Phase 2

1. register-page preference field
2. setup-page explanation
3. persistent switcher in logged-in nav

## Success conditions

1. users notice that mode selection changed the site
2. the changed nav still feels like the same system
3. non-experts are led into literature exploration first
4. theory/mechanism-oriented users can get faster access to those areas
5. switching mode is easy and reversible

## Immediate implementation note

This component should be implemented against the existing KA pages rather than waiting for a total redesign.
It is a unification feature, not a greenfield replacement.
