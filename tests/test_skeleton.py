"""Skeleton guards — the environment contract from docs/PROJECT_BRIEF.md stays intact."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "data/d0",
    "data/d1",
    "data/d2",
    "data/d3",
    "eval/frozen",
    "eval/dev",
    "eval/results",
    "train/configs",
    "registry",
    "docs",
    "tools",
]

COVERAGE_HEADER = (
    "case_id,status,language,domain,rules_exercised,axis2_band,defect_seeded,"
    "source_grades_present,author_date,salim_verified,reviewer_verdict"
)


def test_required_dirs_exist():
    missing = [d for d in REQUIRED_DIRS if not (ROOT / d).is_dir()]
    assert not missing, f"skeleton dirs missing: {missing}"


def test_coverage_matrix_header_is_the_brief_contract():
    first = (ROOT / "data/d1/coverage_matrix.csv").read_text(encoding="utf-8").splitlines()[0]
    assert first == COVERAGE_HEADER


def test_mandatory_cells_doc_exists():
    assert (ROOT / "data/d1/MANDATORY_CELLS.md").is_file()


def test_gitignore_protects_trade_secret_perimeter():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for pattern in ("*.safetensors", "*.gguf", ".env", "data/**/raw/", "wandb/"):
        assert pattern in gitignore, f"missing .gitignore pattern: {pattern}"
