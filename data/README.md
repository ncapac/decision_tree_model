# Data

Data is stored as immutable, manifest-backed snapshots.

## Layout

- `catalog/` contains import plans and the snapshot index.
- `catalog/<snapshot_id>.report.json` contains generated file-level coverage
  metadata (CSV columns, row counts, date spans, and missingness).
- `snapshots/<snapshot_id>/manifest.json` records source, status, and file hashes.
- `snapshots/<snapshot_id>/files/` contains byte-exact imported inputs.

## Current snapshot

`r15_registered_candidate_2026_10_09` is a provisional copy of inputs currently
pinned by the unfinished R15 registration. It is not the final Round 000 data
snapshot. After R15 closes, the completion record must either promote the exact
same hashes or identify a replacement final snapshot.

## Rules

- Never edit a file inside a completed snapshot.
- Never overwrite a snapshot identifier.
- Acquisition and transformation code belongs in the package, not beside data.
- Scratch arrays, caches, old lab panels, and unused historical sources are not
  migrated by default.
- A round references a snapshot manifest and any round-specific derived dataset;
  it does not silently read whichever file happens to be newest.
- Build a coverage report with
  `python -m decision_tree_model.cli describe-data --snapshot <snapshot_id>`.
  Reports are derived metadata and never replace the manifest as the integrity
  or provenance source of truth.
