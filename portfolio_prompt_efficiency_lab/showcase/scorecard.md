# Comparison Scorecard

Use this during the live run so the audience sees what "efficient" means before you reveal the result.

Run the comparison in two sessions:

- Session 1: discovery + impact analysis
- Session 2: follow-up implementation from a fresh agent session

The point is not only whether the first session works. The point is whether the first session leaves behind reusable context that makes the second session cheaper and safer.

## Session 1

| Proxy | Careless Prompt Run | Disciplined Prompt Run |
| --- | --- | --- |
| Files inspected |  |  |
| Repeated scans of the same area |  |  |
| Turns needed to reach a usable answer |  |  |
| Unrelated files touched |  |  |
| Reusable artifact created or reused |  |  |
| Clear risk summary provided |  |  |

## Session 2

| Proxy | Careless Prompt Run | Disciplined Prompt Run |
| --- | --- | --- |
| Files inspected |  |  |
| Repeated scans of the same area |  |  |
| Turns needed to reach a usable answer |  |  |
| Unrelated files touched |  |  |
| Reused artifacts from session 1 |  |  |
| Tests run before claiming success |  |  |
| Clear risk summary provided |  |  |

## Combined metrics

| Proxy | Careless Prompt Run | Disciplined Prompt Run |
| --- | --- | --- |
| Total request turns across both sessions |  |  |
| Total search/read churn across both sessions |  |  |
| Total validation commands across both sessions |  |  |
| Uncached prompt tokens across both sessions |  |  |

## Facilitator note

The goal is not to make the careless run fail. The goal is to make the disciplined run visibly more bounded, more reusable across sessions, and easier to trust.
