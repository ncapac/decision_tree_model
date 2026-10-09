# Command and workflow design

The old project accumulated round-specific scripts. This project uses one CLI
over reusable package workflows.

## Public command surface

After installation, use `dtm`:

```powershell
dtm validate-round --round round_000
dtm build-index
dtm import-data --source-root <path> --plan <path>
dtm create-completion-record --source-root <path> --inventory <path> `
  --output <path>
dtm recover-legacy --round round_000 --source-root <path> `
  --completion-record <path>
dtm build-notebook --round round_000
```

`python -m decision_tree_model` exposes the same commands.

Completion-record creation validates and hashes the selected source artifacts by
default. Writing requires both `--execute` and `--confirm-source-complete`.

## Structure

- `src/decision_tree_model/cli.py` parses arguments and prints outcomes.
- `src/decision_tree_model/workflows/` contains testable orchestration.
- Domain packages contain portfolio, state, policy, and evaluation behavior.
- Round configuration supplies experimental choices.
- There is no top-level script collection. Durable commands use the package CLI.

## Rules

- Never create `run_round_17.py` or an equivalent round-numbered script.
- Add a CLI subcommand only for a durable user operation.
- Put one-off migration behavior in an isolated workflow with a removal condition.
- Commands validate by default; destructive or materializing behavior requires an
  explicit flag such as `--execute`.
- Paths are command inputs or project-relative configuration, never constants.
- Workflow functions return typed results and do not depend on console output.

## Native round execution

The native execution API is intentionally not scaffolded before R15 closes.
Designing it from an unfinished source round would encode temporary R15 details.
It will be added after the final R15 capability extraction, using domain stages
rather than one script per research phase.
