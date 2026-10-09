# R15 capability migration inventory

This inventory is capability-based. It is not a file-copy list, and all
implementation decisions remain provisional until R15 closes.

| Capability | Current source area | New-project treatment |
|---|---|---|
| configuration and paths | `src/config.py`, round YAML | specify a small typed config model; do not copy accumulated keys |
| portfolio recurrence | `src/engine/portfolio*.py` | reimplement from explicit recurrence; regression-test against frozen traces |
| exact FX overlay | `src/engine/fx_overlay.py`, `src/evo/tape.py` | preserve economic identities and ledger tests; extract code only after review |
| feasibility constraints | `src/optimizer/constraints.py` | rewrite as a focused domain service with grid and exposure contracts |
| CPCV geometry | `src/evo/cpcv*.py` | retain methodology; consolidate duplicated split/evaluation paths |
| decision clocks | `src/evo/clock.py`, execution convention | define one clock abstraction with explicit observation, decision, and pricing rows |
| split base fitting | `src/evo/base_fit.py` | migrate the final algorithm through a generic fitter interface |
| state layer | R15 state modules | recover final fitted state evidence; redesign implementation after R15 freezes |
| action/policy layer | policy modules and R15 amendments | separate action vocabulary, objective, search, and execution; no round names |
| held-out evaluation | held-out, OOF, path modules | one evaluation API with date-level aggregation and reconciliation contracts |
| provenance | `src/evo/provenance.py` | implement natively and include repo, superproject, environment, and input hashes |
| result loading | `src/evo/results_store.py` | replace reserved-filename heuristics with manifest-declared schemas |
| notebooks | generated/archived notebooks | do not migrate; build one presentation template over manifests |
| round runners | `scripts/evo_r*.py` | do not migrate; replace with CLI stages and registered workflow definitions |
| old node libraries | `nodes_r*.py`, legacy actions | do not migrate wholesale; admit only final active vocabulary through typed registries |
| premium/static line | `src/predictive/`, old optimizer research | exclude from active project |
| historical methodology | plans, handoffs, diary, archives | keep in old repo; import only final R15 interpretation artifacts |

## Decision test for code extraction

Existing code is extracted only if all are true:

1. it implements final R15 behavior rather than an obsolete round;
2. it is round-independent after removing configuration;
3. it has strong tests that distinguish correct from plausible-wrong behavior;
4. its dependencies fit the new architecture;
5. extraction is clearer and safer than clean-room reimplementation.

Otherwise, preserve the contract and regression evidence and write the new
implementation in this repository.

## Deferred decisions

The exact state model, action objective, final artifact inventory, and native
round execution stages remain deferred because R15 is not complete.
