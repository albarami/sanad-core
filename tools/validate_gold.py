"""Validate a Sanad D1 gold record (PLAN v2, Slice 1).

Usage:
    uv run python -m tools.validate_gold data/d1/gold-0001.json [--emit-coverage]

Exit codes: 0 = Tier-A + Tier-B pass (Tier-C warnings are non-blocking);
1 = Tier-A (schema) failure; 2 = Tier-B (derivation-completeness) failure;
3 = usage / file error.
"""

from __future__ import annotations

import argparse
import json
import sys

from pydantic import ValidationError

from tools.sanad_schema import (
    COVERAGE_HEADER,
    GoldRecord,
    coverage_row,
    tier_b_failures,
    tier_c_warnings,
)


def validate_path(path: str, *, emit_coverage: bool = False, reviewer_verdict: str = "pending") -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR reading {path}: {exc}", file=sys.stderr)
        return 3

    # Tier-A — schema + numeric consistency + coverage invariant (pydantic).
    try:
        rec = GoldRecord.model_validate(data)
    except ValidationError as exc:
        print(f"TIER-A FAIL — schema invalid ({path}):", file=sys.stderr)
        print(exc, file=sys.stderr)
        return 1
    print(f"TIER-A pass — {rec.record_id} constructs and satisfies numeric + coverage invariants")

    # Tier-B — derivation-trace completeness (structured fields only).
    b_fails = tier_b_failures(rec)
    if b_fails:
        print("TIER-B FAIL — derivation-trace completeness:", file=sys.stderr)
        for f in b_fails:
            print(f"  - {f}", file=sys.stderr)
        return 2
    print(f"TIER-B pass — {len(rec.target.verdicts)} verdict(s) cite band-producing rules")

    # Tier-C — evidence cross-checks (non-blocking this slice).
    for w in tier_c_warnings(rec):
        print(f"TIER-C warn — {w}")

    if emit_coverage:
        print("\n# coverage_matrix.csv")
        print(COVERAGE_HEADER)
        print(coverage_row(rec, reviewer_verdict=reviewer_verdict))

    print(f"\nVALID: {rec.record_id}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a Sanad D1 gold record.")
    ap.add_argument("path", help="path to a gold-NNNN.json record")
    ap.add_argument(
        "--emit-coverage",
        action="store_true",
        help="print the coverage_matrix.csv header + row derived from the record",
    )
    ap.add_argument(
        "--reviewer-verdict",
        default="pending",
        help="reviewer_verdict value for the emitted coverage row (default: pending)",
    )
    args = ap.parse_args()
    return validate_path(
        args.path, emit_coverage=args.emit_coverage, reviewer_verdict=args.reviewer_verdict
    )


if __name__ == "__main__":
    raise SystemExit(main())
