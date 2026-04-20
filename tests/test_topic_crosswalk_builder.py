from scripts.build_ka_adapter_payloads import build_topic_crosswalk_payload


def test_build_topic_crosswalk_payload_derives_rows_and_indexes():
    topic_hierarchy = {
        "default_view": "defended",
        "source_files": {"topic_hierarchy": "data/ka_payloads/topic_hierarchy.json"},
        "views": {
            "defended": {
                "topics": [
                    {
                        "id": "luminous__affect_negative_stress",
                        "label": "Lighting Conditions -> Stress",
                        "iv_root": "luminous",
                        "iv_root_label": "Lighting Conditions",
                        "iv_node": "luminous.daylight",
                        "iv_label": "Daylight",
                        "dv_focus": "affect.negative.stress",
                        "dv_focus_label": "Stress",
                        "paper_ids": ["PDF-0001", "PDF-0002"],
                        "paper_count": 2,
                        "theories": ["Circadian Lighting"],
                        "sensors": ["HRV"],
                        "fronts": ["Lighting × Stress"],
                    },
                    {
                        "id": "acoustic__affect_negative_stress",
                        "label": "Acoustic Conditions -> Stress",
                        "iv_root": "acoustic",
                        "iv_root_label": "Acoustic Conditions",
                        "iv_node": "acoustic.noise",
                        "iv_label": "Noise",
                        "dv_focus": "affect.negative.stress",
                        "dv_focus_label": "Stress",
                        "paper_ids": ["PDF-0003"],
                        "paper_count": 1,
                        "theories": ["Soundscape Theory"],
                        "sensors": ["EDA"],
                        "fronts": ["Acoustic × Stress"],
                    },
                ]
            },
            "working": {
                "topics": [
                    {
                        "id": "luminous__affect_negative_stress",
                        "paper_ids": ["PDF-0001", "PDF-0002", "PDF-0004"],
                        "paper_count": 3,
                    }
                ]
            },
        },
    }

    payload = build_topic_crosswalk_payload(topic_hierarchy)

    assert payload["summary"] == {
        "row_count": 2,
        "outcome_count": 1,
        "iv_root_count": 2,
        "default_view": "defended",
        "source_kind": "topic_crosswalk",
    }
    assert [row["topic_id"] for row in payload["rows"]] == [
        "luminous__affect_negative_stress",
        "acoustic__affect_negative_stress",
    ]
    assert payload["rows"][0]["working_paper_count"] == 3
    assert payload["rows"][0]["defended_paper_count"] == 2
    assert payload["rows"][0]["evidence_status"] == "defended"

    assert payload["outcome_index"] == [
        {
            "outcome_term_id": "affect.negative.stress",
            "outcome_label": "Stress",
            "paper_count": 3,
            "topic_ids": [
                "acoustic__affect_negative_stress",
                "luminous__affect_negative_stress",
            ],
            "topic_count": 2,
        }
    ]
    assert payload["iv_root_index"] == [
        {
            "iv_root": "luminous",
            "iv_root_label": "Lighting Conditions",
            "paper_count": 2,
            "topic_ids": ["luminous__affect_negative_stress"],
            "topic_count": 1,
        },
        {
            "iv_root": "acoustic",
            "iv_root_label": "Acoustic Conditions",
            "paper_count": 1,
            "topic_ids": ["acoustic__affect_negative_stress"],
            "topic_count": 1,
        },
    ]
