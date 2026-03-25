# Duplicate Page Dispositions

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`

## Purpose

List overlapping page families and assign an initial disposition so builders stop treating all duplicates as equal.

## 1. Hypothesis Builder

Pages:
- `ka_hypothesis_builder.html`
- `Designing_Experiments/hypothesis_builder.html`

Disposition:
- `ka_hypothesis_builder.html` = main Atlas / shared canonical surface for now
- `Designing_Experiments/hypothesis_builder.html` = course/studio variant pending merge or retirement

Reason:
- the root KA page is already integrated into the main site family
- the embedded DE page should only remain if it serves a distinct pedagogical purpose

## 2. Instrument / sensor reference surfaces

Pages:
- `ka_sensors.html`
- `Designing_Experiments/sensor_catalogue.html`
- `Designing_Experiments/measurement_instruments.html`

Disposition:
- `ka_sensors.html` = canonical main Atlas reference surface
- embedded DE pages = course-support or legacy until merged

Reason:
- the root KA page already speaks the main product language
- the course pages may still hold useful pedagogy, but should not compete as equal atlas entry points

## 3. Research navigation / experiment navigation

Pages:
- `ka_topics.html`
- `ka_gaps.html`
- `ka_question_maker.html`
- `Designing_Experiments/knowledge_navigator.html`

Disposition:
- root KA pages = canonical main Atlas browse/question surfaces
- `knowledge_navigator.html` = strong course/studio concept that should inform the main IA, but not remain a parallel front door indefinitely

Reason:
- the main site now already has topic, gap, and question entry points
- the embedded course page is conceptually strong but duplicative as a separate primary navigator

## 4. Experiment design studio

Pages:
- `ka_hypothesis_builder.html`
- `Designing_Experiments/experiment_wizard.html`
- `Designing_Experiments/theory_and_experiment_design.html`
- `Designing_Experiments/methods_taxonomy.html`

Disposition:
- keep as a course/studio family for now
- do not try to collapse them all immediately
- define later whether a Streamlit-based studio should absorb these functions

Reason:
- these are pedagogically heavy and still useful for the class
- premature merging would create churn without enough product clarity

## 5. Network navigators

Pages:
- `Designing_Experiments/en_navigator.html`
- `Designing_Experiments/bn_navigator.html`

Disposition:
- course/studio specialized tools for now
- candidates for later promotion into the main Atlas only after live data contracts are ready

Reason:
- these are not yet the simplest main entry surfaces
- they are better treated as advanced tools than as top-level public navigation

## 6. Contributor tagging flow

Pages:
- `ka_tagger.html`
- `ka_tag_assignment.html`

Disposition:
- keep both
- promote them visibly inside the main contributor IA now

Reason:
- these are not duplicates; they are a paired workflow that was simply under-integrated

## Working rule

When a duplicate exists, prefer:
1. the page already integrated into the main KA navigation
2. the page with the clearer role in the current product
3. the page that best matches the near-term class and rebuild plan

Do not keep two pages as silent co-canonical surfaces.
