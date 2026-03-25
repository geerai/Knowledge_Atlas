# GUI Data Contracts

Date: 2026-03-24
Repo: `/Users/davidusa/REPOS/Knowledge_Atlas`
Purpose: first-pass contracts for the pages that should receive rebuilt content first

## Contract 1 — Topics
Target page:
- `ka_topics.html`

Required fields per topic:
- `topic_id`
- `topic_label`
- `topic_family`
- `topic_question`
- `paper_count`
- `claim_count`
- `priority_score`
- `evidence_strength_summary`
- `top_papers[]`
- `example_findings[]`
- `method_summary`
- `theory_frame_summary`
- `provisional_flag`

Notes:
- this can be driven initially from finding clusters plus paper metadata
- topic cards should not require full perfect theory fidelity to launch

## Contract 2 — Evidence Browser
Target page:
- `ka_evidence.html`

Required fields per evidence row:
- `paper_id`
- `paper_title`
- `claim_id`
- `claim_text`
- `antecedent`
- `consequent`
- `direction_of_effect`
- `sample_n`
- `evidence_strength_class`
- `method_conditioned_class`
- `paper_theory_frame`
- `structured_result_row`
- `abstract_clean_text`
- `abstract_surface_link`
- `source_pages[]`
- `figure_table_refs[]`
- `provisional_flag`

## Contract 3 — Article detail
Target page:
- new or adapted article-detail surface

Required fields:
- `paper_id`
- `paper_title`
- `citation`
- `abstract_clean_text`
- `theory_frame`
- `methods_plain`
- `methods_exact`
- `stimulus_description`
- `measure_description`
- `method_choice_rationale`
- `structured_results[]`
- `visual_artifacts[]`
- `subject_count_total`
- `subject_count_by_substudy`
- `evidence_profile_summary`
- `provisional_flag`

## Contract 4 — Gaps
Target page:
- `ka_gaps.html`

Required fields per gap:
- `gap_id`
- `gap_type`
- `gap_label`
- `gap_summary`
- `priority_score`
- `linked_topics[]`
- `linked_papers[]`
- `why_open`
- `what_is_missing`
- `possible_next_study`
- `provisional_flag`


## Contract 5 — Theory Guides
Target pages:
- future Theory Explorer / theory-guide surfaces

Required fields for current theory guide:
- `theory_id`
- `theory_name`
- `tier`
- `plain_language_summary`
- `core_commitments[]`
- `best_explained_domains[]`
- `key_support_patterns[]`
- `main_limitations[]`
- `related_theories[]`
- `current_status`
- `design_implications[]`
- `guide_confidence`

Required fields for older theory guide:
- `theory_id`
- `theory_name`
- `tier`
- `historical_role`
- `what_it_got_right[]`
- `what_it_got_wrong[]`
- `why_the_field_moved_on`
- `what_replaced_it[]`
- `what_survives[]`
- `where_it_still_has_influence`
- `guide_confidence`

Notes:
- T1 guides should present current preferred frameworks.
- T1.5 should include a distinct `Older Theories` subsection rather than silently dropping older but influential theories.
- theory guides must be explicit about supersession and survival.

## Contract 6 — Mechanism Guides / Mechanism Explorer
Target pages:
- future Mechanism Explorer / mechanism-guide surfaces

Required fields for mechanism guide:
- `mechanism_id`
- `mechanism_name`
- `mechanism_family`
- `plain_language_summary`
- `entities_or_systems[]`
- `activities_or_steps[]`
- `inputs[]`
- `outputs[]`
- `measurement_surface[]`
- `directly_tested_vs_inferred`
- `maturity_level`
- `linked_theories[]`
- `linked_topics[]`
- `example_papers[]`
- `key_limitations[]`
- `guide_confidence`

Required fields for mechanism claim row:
- `paper_id`
- `claim_id`
- `mechanism_claim_text`
- `mechanism_role`
- `mechanism_chain[]`
- `direct_evidence_surface[]`
- `mediation_or_moderation_type`
- `is_discussion_level_inference`
- `confidence`

Notes:
- mechanism pages must distinguish:
  - directly tested pathways
  - mediation/moderation claims
  - discussion-level inferred pathways
- a cited theory must not be rendered as if it automatically proves a mechanism
- mechanism writing should follow the extraction discipline in:
  - `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/docs/CHEAT_SHEET_MECHANISM_MEDIATION_2026-03-21.md`

## Contract 7 — Neural Underpinnings Explorer
Target pages:
- future Neural Underpinnings Explorer / pathway pages

Required fields for pathway guide:
- `pathway_id`
- `pathway_name`
- `plain_language_summary`
- `systems_involved[]`
- `key_steps[]`
- `directly_measured_steps[]`
- `inferred_steps[]`
- `linked_theories[]`
- `linked_mechanisms[]`
- `linked_topics[]`
- `classic_papers[]`
- `follow_on_papers[]`
- `current_limitations[]`
- `measurement_options[]`
- `guide_confidence`

Required fields for reading-list panel:
- `pathway_id`
- `classic_anchor_papers[]`
- `recent_reviews[]`
- `direct_measurement_papers[]`
- `why_each_matters[]`
- `collection_status`

Notes:
- this layer should begin from panel-proposed pathway families
- it should explicitly support article-finder work
- it should distinguish classic anchors from later expansion papers
- it should use progressive disclosure rather than dumping full pathway detail immediately

## Status flags

Every contract should support these visible status fields where relevant:
- `provisional_flag`
- `rebuild_run_id`
- `constructed_from_article`
- `theory_tentative`
- `subject_count_missing`
- `result_structure_partial`

## Rule

A page may launch before all optional fields are populated.
A page should not hide when a field is missing or constructed.
