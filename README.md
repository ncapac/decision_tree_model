# Decision Tree Model

This repository is a clean, single-purpose decision-tree research platform built to replace the historical experimental workspace.

It is intentionally not a copy of the previous project. The project history in the old workspace remains the source of scientific evidence and legacy round artifacts; this repository defines the new operational boundary.

## Mission

The active objective is to operate a disciplined, reproducible decision-tree research workflow with:

- round-based registration and evaluation
- clear provenance and artifact tracking
- reusable infrastructure not tied to any single round
- a clean results index by round
- neutral handling of legacy rounds, especially imported historical work

## Design principles

1. The old repo is historical evidence, not a codebase to inherit by default.
2. This project is round-aware but round-agnostic in its infrastructure.
3. Each round has a clear contract: registration, artifacts, evaluation, provenance, and presentation.
4. Big experiment output is indexed and validated, not buried inside scripts or notebooks.
5. Legacy rounds are imported under explicit recovery rules and retained as immutable evidence.

## Round 0 policy

Round 0 is reserved for recovering R15 after R15 is complete. It currently
contains only a pending recovery manifest; no R15 result has been imported.

This means:

- the imported round is treated as recovered legacy data, not as a fresh design;
- the scientific result remains attributable to the original round;
- the new project defines the platform independent of that historical implementation;
- future rounds are built on the new platform, not on old assumptions.

## Repository layout

- `config/` — project defaults and round registrations.
- `data/` — immutable, manifest-backed input snapshots.
- `docs/` — architecture, methodology, protocol, and artifact contracts.
- `src/decision_tree_model/` — reusable platform code.
- `src/decision_tree_model/cli.py` — the single command surface.
- `results/` — complete per-round evidence, notebooks, and the generated index.
- `tests/` — contract and regression tests.

## Operational rules

- no hardcoded absolute paths
- no notebook execution as the main research engine
- no round-specific logic in shared infrastructure
- all artifacts must be indexed and versioned
- all imported historical results must record their original provenance
- scientific claims must be supported by machine-readable evidence

## Quick start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
dtm validate-round --round round_000
```

## Contributing

This project deliberately keeps the core infrastructure small and opinionated. Add functionality only when it is:

- reusable across rounds,
- tested,
- documented,
- clearly separated from round-specific experiments.
