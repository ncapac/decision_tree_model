# Documentation map

Documentation is organized by authority, not by chronology.

| Document | Authority | Purpose |
|---|---|---|
| `architecture.md` | platform | component boundaries and dependency direction |
| `methodology.md` | platform | scientific invariants shared by rounds |
| `research_protocol.md` | platform | lifecycle and held-out-read discipline |
| `artifact_contract.md` | platform | manifest, hash, and evidence rules |
| `data_architecture.md` | platform | immutable shared input snapshots |
| `script_and_cli_design.md` | platform | command and workflow organization |
| `documentation_system.md` | platform | ownership, status, and migration rules |
| `migration_plan.md` | migration | boundary between old and new repositories |
| `migrations/r15_to_round_000.md` | migration | gated R15 recovery checklist |
| `migrations/r15_capability_inventory.md` | migration | capability-level migration decisions |

## Authority order

1. Validated machine-readable round manifests and artifacts.
2. The owning round's resolved registration and decision record.
3. Stable platform contracts in this directory.
4. Migration notes.
5. Historical material in the old repository.

Plans state intent. They are not evidence that a run finished or a result exists.

## Status language

Use these terms literally:

- **planned**: proposed but not implemented;
- **registered**: frozen before execution;
- **pending**: waiting for a prerequisite;
- **measured**: supported by a named artifact;
- **imported**: copied and hash-verified from another repository;
- **reproduced**: generated again by a new execution;
- **closed**: no further changes are allowed within that round.
