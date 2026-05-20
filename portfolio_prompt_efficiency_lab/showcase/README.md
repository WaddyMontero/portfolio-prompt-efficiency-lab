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

For exported Copilot/Codex JSON logs, use the analyzer from the facilitator repo root:

```bash
python3 scripts/analyze_agent_export.py /path/to/first_export.json [/path/to/second_export.json]
```

It extracts scorecard-style metrics such as request turns, search/read churn, edited files, validation commands, and uncached prompt tokens.
