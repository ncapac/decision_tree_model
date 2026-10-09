# Workspace rules

This is a clean, single-purpose decision-tree research platform. The old
`kiss_etf_optimizer` repository is evidence and history, not a code template.

## Non-negotiable boundaries

- Work inside this repository unless the user explicitly authorizes another path.
- Never edit the old repository as part of migration planning or recovery.
- Do not copy old code, scripts, documentation, or notebooks by default.
- Shared code must be round-agnostic. Round-specific choices belong in round data.
- Use repository-relative paths resolved through project configuration.
- Generated evidence is valid only when listed in a validated manifest.
- Notebooks present persisted evidence; they never fit, search, or rerun research.

## Before changing a subsystem

Read its nearest `CLAUDE.md`, then the relevant contract under `docs/`.
Hierarchical files add local rules without repeating this file.

## Validation

Run the smallest relevant tests. Contract changes must test both acceptance and
rejection. A recovery workflow must default to validation-only and require an
explicit execution flag.

## Current migration state

R15 is unfinished. `results/round_000` is reserved but contains no imported R15
result.
Do not mark it recovered, create a results notebook, or state an R15 result until
the source-completion record passes the recovery gate.
