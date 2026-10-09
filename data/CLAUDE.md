# Data rules

- Data snapshots are immutable after their manifest is written.
- Validate all hashes before copying and write the manifest last.
- Use a new snapshot identifier for changed bytes.
- Provisional snapshots cannot support final or measured claims.
- Do not add acquisition scripts, caches, or experiment scratch arrays here.
- Record units, frequency, publication timing, and causality metadata before a
  dataset becomes a native project input.
