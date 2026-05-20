from __future__ import annotations

import os
import subprocess
from pathlib import Path

from reset_demo_state import clean_runtime_artifacts, restore_baseline_files


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    env = os.environ.copy()
    env.setdefault("DBT_PROFILES_DIR", ".")
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def main() -> None:
    restore_baseline_files()
    clean_runtime_artifacts()

    run(["dbt", "seed"])
    run(["dbt", "build"])


if __name__ == "__main__":
    main()
