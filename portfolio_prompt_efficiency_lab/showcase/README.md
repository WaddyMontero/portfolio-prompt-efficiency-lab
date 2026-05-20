# Showcase Pack

This folder holds the materials for the live comparison between careless and disciplined prompting.

The recommended format is a two-session exercise:

- session 1: discovery and impact analysis
- session 2: follow-up implementation from a fresh agent session

- [prompt_pairs.md](prompt_pairs.md): exact prompts for the three tasks
- [scorecard.md](scorecard.md): visible proxies to compare the runs
- [facilitator_guide.md](facilitator_guide.md): timing and steering notes for the live demo
- [reference_solution.md](reference_solution.md): bounded expectations for the implementation task
- [live_demo_one_pager.md](live_demo_one_pager.md): compact handout appendix for the workshop

For exported Copilot/Codex JSON logs, use `python scripts/analyze_agent_export.py <export.json> [second_export.json]` from the repo root to extract scorecard-style metrics.
