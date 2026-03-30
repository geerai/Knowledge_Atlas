# HTML Surface Manifest

Date: 2026-03-30

This is the clean working grouping of the visible HTML surfaces in the `Knowledge_Atlas` family.
It excludes generated article HTML, Mathpix artifacts, Zotero captures, and other non-site debris.

## Knowledge Atlas: Public and Research Surfaces

- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_home.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_topics.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_topic_hierarchy.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_evidence.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_argumentation.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_gaps.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_interpretation.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_warrants.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_sensors.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_article_search.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_sitemap.html`

## Knowledge Atlas: Contributor and Operations Surfaces

- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_articles.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_article_propose.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_contribute.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_annotations.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_tagger.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_tag_assignment.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_approve.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_dashboard.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_workflow_hub.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_datacapture.html`

## Knowledge Atlas: Account and Course Shell

- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_login.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_register.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_reset_password.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_forgot_password.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_student_setup.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_user_home.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_schedule.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_thursday_tasks.html`

## COGS 160 / AI / VR / Experiment Design

- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_ai_methodology.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_article_finder_assignment.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_gui_assignment.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/ka_vr_assignment.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/fall160_schedule.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/cogs160_spring_2026_site.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/course_pilot.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/experiment_wizard.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/hypothesis_builder.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/sensor_catalogue.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/measurement_instruments.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/methods_taxonomy.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/knowledge_navigator.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/bn_navigator.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/en_navigator.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/system_inventory.html`
- `/Users/davidusa/REPOS/Knowledge_Atlas/Designing_Experiments/theory_and_experiment_design.html`

## Not Part of the Live Sites

These are real HTML files in the repository, but they should not be confused with the site surfaces above.

- Generated article HTML under `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/data/science_writer_articles`
- Mathpix and verification HTML under `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/data/verification_runs`
- Zotero and bibliography captures under `/Users/davidusa/REPOS/__Zotero whole bibliography` and `/Users/davidusa/REPOS/_Collecting Articles`
- BN frontends under `/Users/davidusa/REPOS/BN/frontend` and `/Users/davidusa/REPOS/BN_graphical/frontend`

## HTML Generation and Frontend Engines

The main Knowledge Atlas site is not React-based. It is static HTML and JavaScript fed by JSON payloads generated from:

- `/Users/davidusa/REPOS/Knowledge_Atlas/scripts/build_ka_adapter_payloads.py`

There are React or Vite frontends elsewhere in the repo:

- `/Users/davidusa/REPOS/emotibit_polar_data_system/frontend/package.json`
- `/Users/davidusa/REPOS/BN_graphical/frontend-v2/package.json`

There are also server-rendered HTML templates in the Article Eater codebase:

- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/src/gui/templates`
- `/Users/davidusa/REPOS/Article_Eater_PostQuinean_v1_recovery/apps/user_rules_gui/templates`
