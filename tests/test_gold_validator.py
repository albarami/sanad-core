"""Unit tests for the D1 gold-record schema + validator (PLAN v2, Slice 1)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from tools.sanad_schema import (
    GoldRecord,
    coverage_row,
    find_unresolved_placeholders,
    tier_b_failures,
)
from tools.validate_gold import validate_path

REPO_ROOT = Path(__file__).resolve().parents[1]
GOLD1 = REPO_ROOT / "data" / "d1" / "gold-0001.json"
GOLD2 = REPO_ROOT / "data" / "d1" / "gold-0002.json"
SCHEMA_JSON = REPO_ROOT / "data" / "d1" / "gold.schema.json"

EXPECTED_COVERAGE_ROW = (
    "gold-0001,gold_approved,en,islamic_finance:sukuk_certification,"
    "R1;R2;R3;R4;R5,V1;V6,shudhudh,S1;S3;S4;MATRUK,2026-07-05,yes,approved"
)

EXPECTED_COVERAGE_ROW_GOLD2 = (
    "gold-0002,gold_approved,ar,islamic_finance:sukuk_certification,"
    "R1;R2;R3;R6,V2;V3;V4,ilal,S3;S4;S5;S6,2026-07-06,yes,approved"
)


def base() -> dict:
    return json.loads(GOLD1.read_text(encoding="utf-8"))


def base2() -> dict:
    return json.loads(GOLD2.read_text(encoding="utf-8"))


# 1 — the real record is valid through Tier-A + Tier-B, and validate_path exits 0
def test_gold_0001_validates():
    rec = GoldRecord.model_validate(base())
    assert rec.record_id == "gold-0001"
    assert tier_b_failures(rec) == []
    assert validate_path(str(GOLD1)) == 0


# 2 — score outside its band
def test_score_outside_band_rejected():
    d = base()
    d["target"]["verdicts"][0]["score"] = 70  # V1 requires 90–100
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 3 — band / grade-name disagreement
def test_band_grade_mismatch_rejected():
    d = base()
    d["target"]["verdicts"][0]["grade"] = "mawdu"  # band is V1 → expects sahih
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 4 — Axis-1 score outside its grade band
def test_axis1_grade_score_mismatch_rejected():
    d = base()
    d["input"]["sources"][0]["axis1_score"] = 63  # S1 requires 90–100
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 5 — missing a required top-level key
def test_missing_top_level_key_rejected():
    d = base()
    del d["meta"]
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 6 — empty derivation_trace
def test_empty_derivation_trace_rejected():
    d = base()
    d["target"]["verdicts"][0]["derivation_trace"] = []
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 7 — empty rules_cited
def test_empty_rules_cited_rejected():
    d = base()
    d["target"]["verdicts"][0]["rules_cited"] = []
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 8 — meta.rules_exercised != union(verdict.rules_cited)
def test_rules_exercised_mismatch_rejected():
    d = base()
    d["meta"]["rules_exercised"] = ["R1", "R2", "R4", "R5"]  # drops R3, still in union
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 9 — meta.defects_seeded != union(verdict.defect_mechanisms)
def test_defects_seeded_mismatch_rejected():
    d = base()
    d["meta"]["defects_seeded"] = []  # rejection verdict still carries shudhudh
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 10 — Tier-B: a V6 verdict that does not cite R3 (Tier-A kept satisfiable)
def test_v6_without_r3_tier_b_fails():
    d = base()
    rej = d["target"]["verdicts"][2]
    rej["rules_cited"] = ["R1"]
    del rej["defect_mechanisms"]
    d["meta"]["rules_exercised"] = ["R1", "R2", "R4", "R5"]
    d["meta"]["defects_seeded"] = []
    rec = GoldRecord.model_validate(d)  # Tier-A now passes
    fails = tier_b_failures(rec)
    assert any("must cite R3" in f for f in fails)


# 11 — Tier-B: a V6 verdict with no fabrication signal
def test_v6_without_fabrication_signal_tier_b_fails():
    d = base()
    d["target"]["escalation"]["fraud_alert"]["issued"] = False
    rec = GoldRecord.model_validate(d)  # Tier-A passes; no ilal, fraud off
    fails = tier_b_failures(rec)
    assert any("fabrication signal" in f for f in fails)


# 12 — Tier-B: shudhūdh present but band stronger than the V4 cap
def test_shudhudh_above_cap_tier_b_fails():
    d = base()
    ev = d["target"]["verdicts"][0]  # V1 event
    ev["rules_cited"] = ["R1", "R2", "R3", "R4"]
    ev["defect_mechanisms"] = ["shudhudh"]
    rec = GoldRecord.model_validate(d)  # union unchanged {R1..R5}; Tier-A ok
    fails = tier_b_failures(rec)
    assert any("caps verdict at V4" in f for f in fails)


# 13 — Tier-B: a verdict citing only a modifier (no R1/R3 anchor)
def test_modifier_only_verdict_tier_b_fails():
    d = base()
    d["target"]["verdicts"][0]["rules_cited"] = ["R4"]
    d["meta"]["rules_exercised"] = ["R1", "R3", "R4", "R5"]  # keep Tier-A union match
    rec = GoldRecord.model_validate(d)
    fails = tier_b_failures(rec)
    assert any("no band-setting rule" in f for f in fails)


# 14 — invalid enum tokens
def test_invalid_enums_rejected():
    for path, val in (
        (("language",), "fr"),
        (("target", "verdicts", 0, "band"), "V7"),
        (("input", "sources", 0, "axis1_grade"), "S7"),
    ):
        d = base()
        node = d
        for k in path[:-1]:
            node = node[k]
        node[path[-1]] = val
        with pytest.raises(ValidationError):
            GoldRecord.model_validate(d)


# 15 — confidence_interval bounds
def test_ci_bounds_rejected():
    d = base()
    d["target"]["verdicts"][0]["confidence_interval"] = [95, 90]  # lo > hi
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# 16 — the emitted coverage row is exactly the 11-column line
def test_coverage_row_literal():
    rec = GoldRecord.model_validate(base())
    assert coverage_row(rec, reviewer_verdict="approved") == EXPECTED_COVERAGE_ROW
    assert len(EXPECTED_COVERAGE_ROW.split(",")) == 11
    # gold_approved record activates the salim_verified=yes branch
    assert coverage_row(rec).split(",")[9] == "yes"


# 17 — the record validates against the emitted JSON Schema artifact (dev-only)
def test_jsonschema_artifact_roundtrip():
    jsonschema = pytest.importorskip("jsonschema")
    if not SCHEMA_JSON.exists():
        pytest.skip("gold.schema.json not generated yet")
    schema = json.loads(SCHEMA_JSON.read_text(encoding="utf-8"))
    jsonschema.validate(instance=base(), schema=schema)


# extra guard — unknown field is rejected (extra='forbid')
def test_unknown_field_rejected():
    d = base()
    d["surprise"] = 1
    with pytest.raises(ValidationError):
        GoldRecord.model_validate(d)


# extra guard — a Tier-B-broken record makes validate_path exit non-zero
def test_validate_path_tier_b_exit(tmp_path):
    d = base()
    d["target"]["escalation"]["fraud_alert"]["issued"] = False  # V6 loses its signal
    p = tmp_path / "broken.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    assert validate_path(str(p)) == 2


# ── placeholder guard (permanent corpus safeguard) ────────────────────────────


# 18 — find_unresolved_placeholders reports the right paths and is clean otherwise
def test_find_unresolved_placeholders_paths():
    data = {"a": "ok", "b": {"c": "TODO_AR:x"}, "d": ["fine", "TODO_AR:y"], "e": 5}
    assert set(find_unresolved_placeholders(data)) == {"b.c", "d[1]"}
    assert find_unresolved_placeholders({"a": "clean", "b": ["also clean"], "n": 3}) == []


# 19 — the real record #1 carries no placeholders
def test_gold_0001_placeholder_free():
    assert find_unresolved_placeholders(base()) == []


# 20 — a record with any TODO_ stub is rejected (exit 4) before Tier-B / coverage
def test_placeholder_record_rejected_exit4(tmp_path):
    d = base()
    d["input"]["claim"] = "TODO_AR:overall_claim"  # unauthored stub anywhere in the tree
    p = tmp_path / "with_placeholder.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    assert validate_path(str(p)) == 4
    assert validate_path(str(p), emit_coverage=True) == 4  # coverage is never reached


# ── gold-0002 acceptance (runs on Salim's real Arabic draft, never placeholders) ──


# 21 — the Arabic draft validates clean through Tier-A + guard + Tier-B
def test_gold_0002_validates():
    rec = GoldRecord.model_validate(base2())
    assert rec.record_id == "gold-0002"
    assert rec.language.value == "ar"
    assert tier_b_failures(rec) == []
    assert find_unresolved_placeholders(base2()) == []
    assert validate_path(str(GOLD2)) == 0


# 22 — the emitted coverage row is exactly the fixed draft-stage line
def test_gold_0002_coverage_row_literal():
    rec = GoldRecord.model_validate(base2())
    assert coverage_row(rec, reviewer_verdict="approved") == EXPECTED_COVERAGE_ROW_GOLD2
    assert len(EXPECTED_COVERAGE_ROW_GOLD2.split(",")) == 11
    assert coverage_row(rec).split(",")[9] == "yes"  # gold_approved → salim_verified=yes


# 23 — Slice-2 precedent: chronological-impossibility ilal at V4, fraud off, passes Tier-B
def test_v4_ilal_chronological_no_fraud_passes_tier_b():
    rec = GoldRecord.model_validate(base2())
    v3 = rec.target.verdicts[2]
    assert v3.band.value == "V4"
    assert [d.value for d in v3.defect_mechanisms] == ["ilal"]
    assert {r.value for r in v3.rules_cited} == {"R6", "R3"}
    assert rec.target.escalation.fraud_alert.issued is False
    assert tier_b_failures(rec) == []
