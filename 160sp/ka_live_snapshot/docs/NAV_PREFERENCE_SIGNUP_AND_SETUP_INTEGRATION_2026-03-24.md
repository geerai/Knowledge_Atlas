# Nav Preference Signup and Setup Integration

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Audience: CW and other GUI implementers
Purpose: define how adaptive nav preference should flow across anonymous use, registration, login, and student setup

## Goal

Let users get a relevant navbar and landing path without forcing registration first.

Then, when they do register or log in, preserve and refine that preference instead of discarding it.

## Core model

There are two related but distinct concepts:

1. `user_type`
- who the person is in relation to KA

2. `nav_preference`
- which lane should be emphasized first

These should be stored separately.

## Recommended user types

Use:
- `student_explorer`
- `researcher`
- `contributor`
- `instructor`
- `practitioner`
- `theory_mechanism_explorer`

## Recommended nav preferences

Use:
- `explore_literature`
- `build_test_experiments`
- `contribute_atlas`
- `theory_mechanisms`

## Storage model

### Anonymous session

Store in `localStorage`:
- `ka_user_type`
- `ka_nav_preference`
- `ka_nav_preference_timestamp`

### Logged-in user

Add to the stored user object:
- `userType`
- `navPreference`

Current demo session object already lives in:
- `ka_current_user`

So the logged-in object can be extended without changing the basic pattern.

## Precedence rule

Use this order when resolving the active nav mode:

1. explicit in-session selection made on the current visit
2. logged-in user preference from `ka_current_user`
3. anonymous saved preference from localStorage
4. default public mode

## Default public mode

Before any selection:
- primary nav should lead with `Explore the Literature`
- theory and neural routes should still be available but not foregrounded

## Register page changes

### Do not turn registration into a giant new form

Keep it light.

Add one small section:
- `How do you want KA to orient itself for you?`

Suggested control:
- a single select or radio group for `navPreference`

Suggested values:
- `Explore the literature first`
- `Build or test experiments`
- `Contribute to the Atlas`
- `Theory and mechanisms`

Optional:
- if no anonymous preference exists yet, also allow a lightweight `userType` field

## Setup page changes

`ka_student_setup.html` should explain:
1. that KA can adapt navigation by role/preference
2. that students can switch mode at any time
3. that Track 2 students should usually start in:
- `Explore the literature`
4. that Track 4 students may prefer:
- `Build or test experiments`
or
- `Contribute to the Atlas`

## Navbar behavior

Adaptive nav should change:
- order
- emphasis
- featured dropdown items
- recommended landing link

Adaptive nav should not:
- remove major lanes entirely
- hide cross-links
- create a separate hidden site map

## Suggested visible behavior

### Student explorer

Promote:
- Topics
- Evidence
- Gaps
- Course / Studio

### Researcher

Promote:
- Evidence
- Gaps
- Article Search
- Theory Guides
- Neural Underpinnings

### Contributor

Promote:
- Dashboard
- Articles
- Tagging
- Approval

### Theory / mechanism explorer

Promote:
- Theory Guides
- Neural Underpinnings
- Evidence
- Topics

## UI control recommendation

Add a visible lightweight control:
- `Mode: Student explorer`
or
- `Switch mode`

This should remain available after login and after setup.

## Current implementation note

The existing register flow already writes:
- `ka_current_user`
- `ka_logged_in`

So the cleanest implementation is:
1. preserve anonymous preference if present
2. write `userType` and `navPreference` into `ka_current_user` on registration
3. let nav rendering read from the precedence rule above

## What CW should implement first

1. a small anonymous mode selector
2. nav rendering based on localStorage/session preference
3. a minimal register-page preference field
4. setup-page explanation of how the mode system works

This is enough to make the system feel guided without overengineering identity.
