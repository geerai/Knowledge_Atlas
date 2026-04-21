from importlib import reload

import ka_article_endpoints as kae


def test_classifier_backend_falls_back_when_atlas_shared_is_missing():
    def importer(_name):
        raise ModuleNotFoundError("No module named 'atlas_shared'")

    classifier_cls, evidence_cls, backend, note = kae._load_classifier_backend(importer)
    assert backend == "ka_local_fallback"
    assert "atlas_shared" in note

    classifier = classifier_cls()
    evidence = evidence_cls(
        title="Randomized trial of classroom lighting",
        abstract="This study reports methods, participants, intervention, and results.",
        first_page_text="Randomized controlled trial with participants and results.",
    )
    result = classifier.classify(evidence, allow_surface_creation=False)
    assert result.article_type.value == "empirical_research"
    assert result.article_type.confidence >= 0.75
