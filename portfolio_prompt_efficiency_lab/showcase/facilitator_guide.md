# Facilitator Guide

## Timing

- 2 minutes: introduce the repo and define the scorecard
- 4 minutes: session 1 discovery comparison
- 4 minutes: session 1 impact-analysis comparison
- 4 minutes: reset the agent session, then run or walkthrough session 2 implementation
- 1 minute: recap the habits that reduced waste

## Framing line

This is not a benchmark of model intelligence. It is a benchmark of how much unnecessary work your prompt invites now, and how much reusable context your prompt leaves behind for the next session.

## What to point out live

- Careless prompts usually broaden into compliance, archived models, or scratch SQL before they earn that scope.
- Disciplined prompts create and reuse artifacts, then keep expanding one layer at a time.
- The reporting slice is intentionally solvable without touching the unrelated compliance slice.
- Validation matters because a polished explanation without `dbt test` is still a risky answer.
- The strongest contrast usually appears in session 2, when one run has reusable context and the other has to rediscover it.

## If the careless run still looks okay

- Point out the extra files inspected and repeated scans.
- Show whether it recreated context that the disciplined run would have persisted to `AGENTS.md` or `docs/repo_map.md`.
- Compare the specificity of the implementation plan before any edits happened.
- Emphasize combined metrics across both sessions, not only the first-session output quality.

## If the disciplined run asks for more scope

- Reward that if it justifies the need and expands only one layer.
- The showcase is about bounded reasoning, not about never asking for more context.

## Analyzer script

If you export JSON logs from Copilot or Codex after a rehearsal or live run, you can use the analyzer to pull scorecard-style metrics instead of counting them by hand.

Run it from the facilitator repo root:

```bash
python3 scripts/analyze_agent_export.py /path/to/first_export.json [/path/to/second_export.json]
```

What it helps with:

- total request turns
- total search and read churn
- unique vs repeated file inspection
- edited files
- validation commands
- prompt tokens, uncached prompt tokens, and total tokens
- normalized handling of tiny continuation prompts like `proceed`

Recommended use:

- run it once per careless export and once per disciplined export
- use the combined metrics section in `showcase/scorecard.md` for the final comparison
- if the live run is too fast or messy to score in real time, use the script right after the session and summarize the results back to the audience
