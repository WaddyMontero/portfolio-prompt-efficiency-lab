# Facilitator Guide

## Timing

- 2 minutes: introduce the repo and define the scorecard
- 4 minutes: task 1 discovery comparison
- 4 minutes: task 2 impact-analysis comparison
- 4 minutes: task 3 implementation comparison or walkthrough
- 1 minute: recap the habits that reduced waste

## Framing line

This is not a benchmark of model intelligence. It is a benchmark of how much unnecessary work your prompt invites.

## What to point out live

- Careless prompts usually broaden into compliance, archived models, or scratch SQL before they earn that scope.
- Disciplined prompts reuse artifacts and keep expanding one layer at a time.
- The reporting slice is intentionally solvable without touching the unrelated compliance slice.
- Validation matters because a polished explanation without `dbt test` is still a risky answer.

## If the careless run still looks okay

- Point out the extra files inspected and repeated scans.
- Show whether it recreated context that already existed in `docs/repo_map.md`.
- Compare the specificity of the implementation plan before any edits happened.

## If the disciplined run asks for more scope

- Reward that if it justifies the need and expands only one layer.
- The showcase is about bounded reasoning, not about never asking for more context.
