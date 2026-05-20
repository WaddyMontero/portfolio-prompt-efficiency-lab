from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]

REPO_MAP_TEMPLATE = """# Repo Map

Status: starter template for task 1 in the live workshop.

Keep this file short and reusable. The point is to capture stable repo facts without turning this document into a second repository.

## Fill during discovery

- High-level architecture
- Relevant paths for portfolio reporting
- Paths to ignore for the reporting tasks
- Build and validation commands
- Known risky areas or easy-to-widen scope traps
"""

LINEAGE_TEMPLATE = """# dbt Lineage Notes

Status: starter template for task 2 in the live workshop.

Use this file to capture reusable impact-analysis notes after a scoped review. Expand one dependency layer at a time and record only what would save work in the next session.

## Fill during impact analysis

- Changed model or metric under discussion
- Direct upstream dependencies
- Direct downstream consumers
- One-layer expansion only if it materially changes the answer
- Validation steps the implementation run should execute
"""


def write_text(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink(missing_ok=True)


def restore_baseline_files() -> None:
    write_text(ROOT / "docs" / "repo_map.md", REPO_MAP_TEMPLATE)
    write_text(ROOT / "docs" / "dbt_lineage_notes.md", LINEAGE_TEMPLATE)

    for relative_path in [
        "AGENTS.md",
        "docs/portfolio_reporting.md",
    ]:
        remove_path(ROOT / relative_path)


def clean_runtime_artifacts() -> None:
    for relative_path in [
        "target",
        "logs",
        "dbt_packages",
        "portfolio_prompt_efficiency_lab.duckdb",
    ]:
        remove_path(ROOT / relative_path)


def main() -> None:
    restore_baseline_files()
    clean_runtime_artifacts()


if __name__ == "__main__":
    main()
