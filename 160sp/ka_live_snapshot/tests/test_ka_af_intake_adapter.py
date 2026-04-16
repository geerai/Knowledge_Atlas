from scripts.ka_af_intake_adapter import (
    IntakeIdentity,
    IntakeItem,
    IntakeSubmission,
    KAArticleIntakeAdapter,
    derive_submission_credit_status,
)


MINIMAL_PDF = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF\n"


def test_pdf_submission_is_quarantined_and_normalized(tmp_path):
    pdf_path = tmp_path / "2020_Smith_Daylight_Effects.pdf"
    pdf_path.write_bytes(MINIMAL_PDF)

    adapter = KAArticleIntakeAdapter(tmp_path / "quarantine")
    submission = IntakeSubmission(
        submission_id="KA-IN-0001",
        submitted_by=IntakeIdentity(identity_type="student", user_id="u1", track="2"),
        input_mode="pdf_batch",
        items=[IntakeItem(item_id="1", input_mode="pdf_single", local_path=str(pdf_path))],
    )

    result = adapter.process_submission(submission)
    item = result["items"][0]

    assert item["validation_status"] == "accepted"
    assert item["next_state"] == "staged_pending_review"
    assert item["metadata"]["title"]
    assert item["quarantine"]["quarantine_path"]


def test_citation_submission_is_parsed(tmp_path):
    adapter = KAArticleIntakeAdapter(tmp_path / "quarantine")
    submission = IntakeSubmission(
        submission_id="KA-IN-0002",
        submitted_by=IntakeIdentity(identity_type="anonymous"),
        input_mode="citation_list",
        items=[
            IntakeItem(
                item_id="1",
                input_mode="citation_text",
                raw_text="Ledoux, J.E. Cognitive-Emotional Interactions in the Brain. Cogn. Emot. 2008, 3, 267-289. https://doi.org/10.1080/02699930802132356",
            )
        ],
    )

    result = adapter.process_submission(submission)
    item = result["items"][0]

    assert item["validation_status"] == "accepted"
    assert item["metadata"]["doi"] == "10.1080/02699930802132356"


def test_student_identity_counts_for_credit():
    status = derive_submission_credit_status(
        IntakeIdentity(identity_type="student", user_id="u1", track="2")
    )
    assert status["counts_for_student_credit"] is True
    assert status["dashboard_mode"] == "student_progress"
