# Role Pathway Copy Review

Scope: copy review only. No live HTML was edited.

The current role names are mostly sound. The main improvement is consistency: keep the role labels short, make the taglines explicit about user intent, and keep the hub-page purposes distinct so the user knows whether they are in a launch page or a route page.

## Recommended Copy

| Item | Recommended label | Tagline | One-sentence page-purpose copy |
|---|---|---|---|
| Student Explorer | Student Explorer | Explore the evidence landscape before you build in it. | For students orienting themselves in ATLAS, this mode shows what evidence exists, where the gaps are, and which route to start first. |
| Contributor | Contributor | Build the evidence base one verified claim at a time. | For users contributing to the corpus, this mode foregrounds finding articles, tagging claims, and submitting evidence that others can rely on. |
| Theory Explorer | Theory Explorer | Understand mechanism, not only outcome. | For users tracing how claims are explained, this mode foregrounds theory links, warrant structure, and mechanism-level comparison. |
| Practitioner | Practitioner | Evidence-grounded design needs specific, actionable guidance. | For designers and consultants, this mode surfaces readable evidence and topic-level guidance rather than theory-first navigation. |
| Route-aware Next CTA | Next Step → / Complete Route ✓ | Continue along the recommended route without losing your place. | Advance the user to the next routed page, or finish the route at the final step, while preserving workflow context and progress. |
| Mock hub page: `ka_user_home.html` | My ATLAS | Your personal launch point for recommended paths. | This page is the personalized home base: it shows the active role, recommended workflows, resume state, and a quick way to browse freely. |
| Mock hub page: `ka_workflow_hub.html` | Route | Follow one recommended sequence step by step. | This page is the guided route runner: it presents the current workflow, shows progress, and sends the user to the correct next page. |

## Notes

- `Student Explorer`, `Contributor`, `Theory Explorer`, and `Practitioner` are already strong labels; the main need is tighter, more directive taglines.
- The route CTA should stay dynamic: use `Next Step →` for intermediate steps and `Complete Route ✓` at the end.
- The two hub pages should not sound interchangeable. `ka_user_home.html` should read as a personal launch surface; `ka_workflow_hub.html` should read as a single route in progress.
