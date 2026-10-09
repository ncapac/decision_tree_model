# Result and round evidence rules

- `results/round_NNN/` is a complete round evidence boundary, not a source-code
  package.
- Never mutate an artifact after its hash is banked in the round manifest.
- A legacy recovery remains `awaiting_source_completion` until a validated
  source-completion record is available.
- Imported evidence and later reproductions must use separate paths and records.
- Round documentation describes that round only; platform rules belong in `docs/`.
- Round notebooks are presentation-only and read persisted, validated artifacts.
- Generate notebooks from versioned builders; never hand-edit generated notebooks.
- Refuse notebook generation while a round is pending, running, or missing hashes.
