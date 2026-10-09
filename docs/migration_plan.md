# Migration plan

## Scope

This repository is the clean replacement for the old research workspace. It carries forward only the reusable realities of the project and not the historical clutter.

## What migrates

The following are candidates for migration only if they meet the active criteria:

- scientific invariants and methodology
- round contract rules
- portfolio optimization and feasibility logic
- core state and action abstractions
- artifact validation and provenance logic
- reusable evaluation tools

## What does not migrate by default

- historical notebooks and exploratory analysis scripts
- old round-specific scripts not used by the active platform
- deprecated dashboards and timeline tooling
- archived experimental outputs without a direct operational need
- any code tied to a specific earlier round lifecycle without a clean, generic interface

## Recovery procedure

R15 is not complete, so recovery is currently blocked at the source-completion
gate. See `migrations/r15_to_round_000.md` for the exact staged checklist and
`migrations/r15_capability_inventory.md` for code and capability triage.

## Long-term rule

The new repo should become the only active platform. Old code remains available only as archival evidence and only when explicitly referenced by a valid migration or audit workflow.
