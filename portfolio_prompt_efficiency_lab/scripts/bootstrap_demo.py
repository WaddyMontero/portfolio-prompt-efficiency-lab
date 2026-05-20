from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def run(command: list[str]) -> None:
    env = os.environ.copy()
    env.setdefault("DBT_PROFILES_DIR", ".")
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def main() -> None:
    for relative_path in ["target", "logs", "portfolio_prompt_efficiency_lab.duckdb"]:
        remove_path(ROOT / relative_path)

    run(["dbt", "seed"])
    run(["dbt", "build"])


if __name__ == "__main__":
    main()
