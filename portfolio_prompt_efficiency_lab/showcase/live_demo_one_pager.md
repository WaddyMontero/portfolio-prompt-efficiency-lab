# Live Demo One-Pager

## Core message

Prompt quality is mostly context quality. The disciplined prompt does not make the agent smarter; it removes avoidable work and leaves behind context the next session can actually reuse.

## Two-session flow

1. Session 1, discovery: understand the reporting slice, then create reusable working context.
2. Session 1, impact analysis: assess what USD normalization touches.
3. Session 2, follow-up implementation: start a fresh agent session, then add USD metrics and concentration buckets using saved artifacts.

## Efficiency proxies

- fewer files inspected
- fewer repeated scans
- fewer unrelated edits
- better reuse in the next session
- clearer risks before implementation
- validation before claiming success

## Reusable artifacts

- `AGENTS.md`
- `docs/repo_map.md`
- `docs/dbt_lineage_notes.md`

The point is that the disciplined run creates these artifacts on purpose in session 1, then benefits from them in session 2. The careless run should not be told to create them.

## Prompt habit to repeat

Name the scope, name what to ignore, separate diagnosis from edits, and persist useful findings so the next session does not start from zero.
