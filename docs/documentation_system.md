# Documentation system

The migration must reduce documentation entropy rather than copy it.

## Document classes

### Platform contracts

Stable documents under `docs/` describe architecture, methodology, lifecycle,
artifacts, and commands. They must not contain current-round numbers or results.

### Round records

Each `results/round_NNN/` contains only:

- `registration.yaml`: the resolved design that governed execution;
- `manifest.json`: machine-readable state, provenance, and artifact ledger;
- `decision-log.md`: append-only material decisions after registration;
- `README.md`: a short human index;
- `artifacts/`: banked machine-readable evidence;
- `notebooks/`: generated presentation.

An imported round may omit a native registration if its frozen source completion
record points to the original registration and includes it as an artifact.

### Migration records

`docs/migrations/` records one-time mappings between repositories. Migration
documents are retired after acceptance; they never become methodology.

## Source-of-truth rule

Measured claims live in artifacts. Prose explains them and links to them. A
notebook can format or visualize persisted evidence but cannot become the only
place a number exists.

## Old documentation triage

Do not copy an old document wholesale. For each useful statement:

1. classify it as invariant, final-round design, measured evidence, historical
   context, or obsolete;
2. verify its authority against later amendments and artifacts;
3. place it in exactly one destination;
4. link back to the frozen source artifact;
5. omit it if it has no active operational or evidential purpose.

## Change rules

- Update `docs/README.md` when documents are added or retired.
- Platform docs use present tense and describe active behavior.
- Round records preserve decisions without rewriting history.
- Corrections identify the superseded claim and supporting artifact.
- No top-level status essay is allowed to accumulate round history.
