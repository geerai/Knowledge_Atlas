from ka_article_endpoints import _classify_article_payload


def test_shared_classifier_maps_empirical_surface_to_experimental() -> None:
    classification = _classify_article_payload(
        title="Daylight improves alertness in office workers",
        abstract=(
            "An experiment with 72 participants found that daylight exposure "
            "improved alertness and reduced fatigue (p < .01)."
        ),
        text_surface=(
            "Methods\n"
            "Participants completed an office experiment.\n"
            "Results\n"
            "Daylight improved alertness and reduced fatigue, p < .01.\n"
        ),
    )

    assert classification["canonical_article_type"] == "empirical_research"
    assert classification["article_type"] == "experimental"
    assert classification["evidence_stage"] == "pdf_surface_light"


def test_shared_classifier_maps_meta_analysis_title_to_meta_analysis() -> None:
    classification = _classify_article_payload(
        title="Meta-analysis of green space exposure and stress recovery",
        text_surface="Meta-analysis of green space exposure and stress recovery",
    )

    assert classification["canonical_article_type"] == "meta_analysis"
    assert classification["article_type"] == "meta_analysis"
