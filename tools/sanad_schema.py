"""Sanad D1 gold-record schema — the enforced contract (PLAN v2, Slice 1).

Derived from UDS Appendix B (training-record schema) and UDS §2 (dual-axis
grades + derivation rules R1–R6). pydantic v2 is the enforcement layer; a
JSON Schema artifact is emitted from it for documentation/interop
(`python -m tools.sanad_schema` → data/d1/gold.schema.json).

Design commitments (approved PLAN v2):
- `derivation_trace` holds the authored prose verbatim and is NEVER parsed.
  The machine-checkable layer is the structured `rules_cited` /
  `defect_mechanisms` on each Verdict.
- One coverage invariant: meta.rules_exercised (set) == union of every
  verdict's rules_cited (set); likewise defects_seeded vs defect_mechanisms.
- Numeric consistency: every score sits inside its band; every Axis-1 score
  inside its grade band; grade-name and band agree.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


# --------------------------------------------------------------------------
# Enums (UDS §2.2 Axis-1, §2.3 Axis-2, §2.4 rules) — tokens match Appendix B
# --------------------------------------------------------------------------
class Grade(str, Enum):
    """Axis-1 source reliability (Jarḥ wa Taʿdīl), §2.2."""

    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"
    S6 = "S6"
    MATRUK = "MATRUK"


# Axis-1 score bands partition [0, 100]; MATRUK is the < 40 disqualification.
GRADE_RANGE: dict[Grade, tuple[int, int]] = {
    Grade.S1: (90, 100),
    Grade.S2: (80, 89),
    Grade.S3: (70, 79),
    Grade.S4: (60, 69),
    Grade.S5: (50, 59),
    Grade.S6: (40, 49),
    Grade.MATRUK: (0, 39),
}


class Band(str, Enum):
    """Axis-2 claim verdict band (Ṣaḥīḥ ladder), §2.3."""

    V1 = "V1"
    V2 = "V2"
    V3 = "V3"
    V4 = "V4"
    V5 = "V5"
    V6 = "V6"


# Axis-2 score bands partition [0, 100] with no gaps.
BAND_RANGE: dict[Band, tuple[int, int]] = {
    Band.V1: (90, 100),
    Band.V2: (75, 89),
    Band.V3: (60, 74),
    Band.V4: (35, 59),
    Band.V5: (10, 34),
    Band.V6: (0, 9),
}


class Axis2Grade(str, Enum):
    """Classical verdict names bound one-to-one to bands."""

    sahih = "sahih"
    hasan = "hasan"
    hasan_li_ghayrihi = "hasan_li_ghayrihi"
    daif = "daif"
    daif_jiddan = "daif_jiddan"
    mawdu = "mawdu"


BAND_TO_GRADE: dict[Band, Axis2Grade] = {
    Band.V1: Axis2Grade.sahih,
    Band.V2: Axis2Grade.hasan,
    Band.V3: Axis2Grade.hasan_li_ghayrihi,
    Band.V4: Axis2Grade.daif,
    Band.V5: Axis2Grade.daif_jiddan,
    Band.V6: Axis2Grade.mawdu,
}


class Rule(str, Enum):
    """Verdict derivation rules, §2.4."""

    R1 = "R1"  # weakest-link anchor
    R2 = "R2"  # elevation by corroboration
    R3 = "R3"  # demotion by defect
    R4 = "R4"  # ḍabṭ modifier
    R5 = "R5"  # conflict resolution
    R6 = "R6"  # temporal validity


class DefectMechanism(str, Enum):
    shudhudh = "shudhudh"  # anomaly (§5)
    ilal = "ilal"  # hidden-defect / fabrication-class (§6)


class Language(str, Enum):
    en = "en"
    ar = "ar"


class Split(str, Enum):
    train = "train"
    dev = "dev"
    frozen = "frozen"


class ReviewStatus(str, Enum):
    draft = "draft"
    gold_approved = "gold_approved"
    rejected = "rejected"


# --------------------------------------------------------------------------
# Models — `extra="forbid"` everywhere so unknown fields are rejected
# --------------------------------------------------------------------------
_STRICT = ConfigDict(extra="forbid")


class DabtProfile(BaseModel):
    model_config = _STRICT
    composite: float = Field(ge=0.0, le=1.0)
    scope: str


class Source(BaseModel):
    model_config = _STRICT
    source_id: str
    type: str  # recommended vocab in data/d1/SCHEMA.md (extensible, not an enum)
    axis1_grade: Grade
    axis1_score: int = Field(ge=0, le=100)
    dabt_profile: DabtProfile | None = None
    conflict_flags: list[str] | None = None
    upstream_trace: list[str] | None = None
    registry_flags: list[str] | None = None
    content: str
    timestamp: str

    @model_validator(mode="after")
    def _score_in_grade_band(self) -> Source:
        lo, hi = GRADE_RANGE[self.axis1_grade]
        if not (lo <= self.axis1_score <= hi):
            raise ValueError(
                f"axis1_score {self.axis1_score} outside {self.axis1_grade.value} band [{lo}, {hi}]"
            )
        return self


class Context(BaseModel):
    model_config = _STRICT
    jurisdiction: str
    madhab_default: str
    decision_tier: int = Field(ge=1, le=4)


class Verdict(BaseModel):
    model_config = _STRICT
    claim: str
    value: str | None = None
    grade: Axis2Grade
    band: Band
    score: int = Field(ge=0, le=100)
    confidence_interval: list[int] | None = None
    derivation_trace: list[str] = Field(min_length=1)  # authored prose, never parsed
    rules_cited: list[Rule] = Field(min_length=1)  # structured; Tier-B reads this
    defect_mechanisms: list[DefectMechanism] | None = None
    notes: str | None = None
    valid_until: str | None = None

    @model_validator(mode="after")
    def _numeric_and_name_consistency(self) -> Verdict:
        lo, hi = BAND_RANGE[self.band]
        if not (lo <= self.score <= hi):
            raise ValueError(f"score {self.score} outside band {self.band.value} range [{lo}, {hi}]")
        if self.grade != BAND_TO_GRADE[self.band]:
            raise ValueError(
                f"grade {self.grade.value} does not match band {self.band.value} "
                f"(expected {BAND_TO_GRADE[self.band].value})"
            )
        if self.confidence_interval is not None:
            ci = self.confidence_interval
            if len(ci) != 2:
                raise ValueError("confidence_interval must be [lo, hi]")
            clo, chi = ci
            # CI is an uncertainty interval and MAY cross band boundaries;
            # it is only required to bracket the score inside [0, 100].
            if not (0 <= clo <= chi <= 100):
                raise ValueError(f"confidence_interval {ci} must satisfy 0 <= lo <= hi <= 100")
            if not (clo <= self.score <= chi):
                raise ValueError(f"score {self.score} not within confidence_interval {ci}")
        return self


class RegistryUpdate(BaseModel):
    model_config = _STRICT
    source_id: str
    action: str
    pattern: str


class FraudAlert(BaseModel):
    model_config = _STRICT
    issued: bool
    tier: int | None = None


class Escalation(BaseModel):
    model_config = _STRICT
    required: bool
    fraud_alert: FraudAlert | None = None


class GoldInput(BaseModel):
    model_config = _STRICT
    claim: str
    sources: list[Source] = Field(min_length=1)
    context: Context


class GoldTarget(BaseModel):
    model_config = _STRICT
    analysis: str = Field(min_length=1)
    verdicts: list[Verdict] = Field(min_length=1)
    registry_updates: list[RegistryUpdate] = Field(default_factory=list)
    escalation: Escalation


class GoldMeta(BaseModel):
    model_config = _STRICT
    author: str
    drafted_by: str | None = None
    annotation_date: str
    rules_exercised: list[Rule]
    defects_seeded: list[DefectMechanism] = Field(default_factory=list)
    domain: str
    finance_shape: str | None = None
    review_status: ReviewStatus
    preference_pair_ids: list[str] = Field(default_factory=list)


class GoldRecord(BaseModel):
    model_config = _STRICT
    record_id: str = Field(pattern=r"^gold-\d{4}$")
    split: Split
    language: Language
    input: GoldInput
    target: GoldTarget
    meta: GoldMeta

    @model_validator(mode="after")
    def _coverage_invariant(self) -> GoldRecord:
        cited: set[Rule] = set()
        seeded: set[DefectMechanism] = set()
        for v in self.target.verdicts:
            cited |= set(v.rules_cited)
            seeded |= set(v.defect_mechanisms or [])
        if set(self.meta.rules_exercised) != cited:
            raise ValueError(
                f"meta.rules_exercised {sorted(r.value for r in self.meta.rules_exercised)} != "
                f"union(verdict.rules_cited) {sorted(r.value for r in cited)}"
            )
        if set(self.meta.defects_seeded) != seeded:
            raise ValueError(
                f"meta.defects_seeded {sorted(d.value for d in self.meta.defects_seeded)} != "
                f"union(verdict.defect_mechanisms) {sorted(d.value for d in seeded)}"
            )
        return self


# --------------------------------------------------------------------------
# Tier-B — derivation-trace completeness (hard-fail). Reads ONLY the
# structured fields (rules_cited / defect_mechanisms / escalation).
# --------------------------------------------------------------------------
def tier_b_failures(rec: GoldRecord) -> list[str]:
    fails: list[str] = []
    esc = rec.target.escalation
    fraud = bool(esc.fraud_alert and esc.fraud_alert.issued)
    for v in rec.target.verdicts:
        rc = set(v.rules_cited)
        dm = set(v.defect_mechanisms or [])
        tag = v.claim

        # (1) every verdict needs a band-setting rule: R1 (anchor) or R3 (defect/exclusion).
        if not (rc & {Rule.R1, Rule.R3}):
            fails.append(f"{tag}: no band-setting rule (needs R1 or R3); modifiers alone insufficient")

        # (2) any defect mechanism implies R3.
        if dm and Rule.R3 not in rc:
            fails.append(
                f"{tag}: defect mechanism {sorted(d.value for d in dm)} present but R3 not cited"
            )

        # (3) shudhūdh caps at V4; V5/V6 below the cap need a fabrication signal.
        if DefectMechanism.shudhudh in dm:
            if BAND_RANGE[v.band][0] > 35:  # V1/V2/V3 are stronger than the V4 cap
                fails.append(f"{tag}: shudhūdh caps verdict at V4; band {v.band.value} too strong")
            if v.band in (Band.V5, Band.V6) and not (fraud or DefectMechanism.ilal in dm):
                fails.append(
                    f"{tag}: shudhūdh below V4 requires a fabrication signal "
                    f"(fraud_alert.issued or ilal)"
                )

        # (4) a fabricated verdict (V6/mawdu) must cite R3 and carry a fabrication signal.
        if v.band == Band.V6:
            if Rule.R3 not in rc:
                fails.append(f"{tag}: V6/mawdu must cite R3")
            if not (fraud or DefectMechanism.ilal in dm):
                fails.append(
                    f"{tag}: V6/mawdu requires a fabrication signal (fraud_alert.issued or ilal)"
                )
    return fails


# --------------------------------------------------------------------------
# Tier-C — evidence cross-checks (non-blocking WARN this slice).
# --------------------------------------------------------------------------
def tier_c_warnings(rec: GoldRecord) -> list[str]:
    warns: list[str] = []
    # Registry does not exist yet (its slice is later); axis1_grade↔registry match deferred.
    warns.append(
        "registry-grade match deferred: source registry slice not built; "
        "axis1_grade vs registry unchecked"
    )
    if any(Rule.R2 in v.rules_cited for v in rec.target.verdicts):
        roots = [
            s
            for s in rec.input.sources
            if s.axis1_grade in (Grade.S1, Grade.S2, Grade.S3, Grade.S4) and not s.upstream_trace
        ]
        if len(roots) < 2:
            warns.append(
                f"R2 cited but only {len(roots)} independent S4+ root source(s) found (need >=2)"
            )
    if any(Rule.R5 in v.rules_cited for v in rec.target.verdicts) and len(rec.input.sources) < 2:
        warns.append("R5 cited but fewer than 2 sources present")
    return warns


# --------------------------------------------------------------------------
# Coverage-matrix row — the existing 11-column header, no invented columns.
# --------------------------------------------------------------------------
COVERAGE_HEADER = (
    "case_id,status,language,domain,rules_exercised,axis2_band,defect_seeded,"
    "source_grades_present,author_date,salim_verified,reviewer_verdict"
)

_GRADE_ORDER = [Grade.S1, Grade.S2, Grade.S3, Grade.S4, Grade.S5, Grade.S6, Grade.MATRUK]


def coverage_row(rec: GoldRecord, reviewer_verdict: str = "pending") -> str:
    domain = rec.meta.domain
    if rec.meta.finance_shape:
        domain = f"{domain}:{rec.meta.finance_shape}"
    rules = ";".join(r.value for r in rec.meta.rules_exercised)
    bands = ";".join(sorted({v.band.value for v in rec.target.verdicts}))
    defects = ";".join(d.value for d in rec.meta.defects_seeded)
    present = {s.axis1_grade for s in rec.input.sources}
    grades = ";".join(g.value for g in _GRADE_ORDER if g in present)
    salim_verified = "yes" if rec.meta.review_status == ReviewStatus.gold_approved else "no"
    cols = [
        rec.record_id,
        rec.meta.review_status.value,
        rec.language.value,
        domain,
        rules,
        bands,
        defects,
        grades,
        rec.meta.annotation_date,
        salim_verified,
        reviewer_verdict,
    ]
    return ",".join(cols)


def emit_json_schema() -> dict:
    return GoldRecord.model_json_schema()


if __name__ == "__main__":
    import json
    import pathlib

    out = pathlib.Path(__file__).resolve().parents[1] / "data" / "d1" / "gold.schema.json"
    out.write_text(json.dumps(emit_json_schema(), indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}")
