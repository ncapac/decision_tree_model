# Round 000: pending R15 recovery

Round 000 is reserved for a future neutral recovery of R15. R15 is still in
progress, so no result, design, verdict, or source snapshot has been imported.

The files currently in this directory define the recovery contract only.

## Import contract

- R15 must be explicitly declared complete before recovery can begin.
- The source repository revision and source manifest must be frozen first.
- Imported evidence is immutable.
- Recovery normalizes storage and naming but does not reinterpret results.
- A later reproduction is a separate run and never overwrites imported evidence.

## Current state

- `manifest.json` has status `awaiting_source_completion`.
- `artifacts/` is intentionally empty.
- `notebooks/` is intentionally empty.

See `docs/migrations/r15_to_round_000.md` for the gated migration procedure.
