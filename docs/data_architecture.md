# Data architecture

Data and results have different lifecycles and therefore different roots.

The manifests and generated JSON indexes are the current catalog. A relational
database is deliberately not introduced until query volume justifies it; if one
is added later, it must be rebuildable entirely from these manifests.

## Why data is not inside results

A result belongs to one round. A data snapshot can be referenced by multiple
rounds and must remain stable while those rounds are audited or reproduced.
Putting data under a round would either duplicate bytes or make later rounds
depend on another round's directory.

## Layout

```text
data/
  catalog/
    index.json
    <snapshot>.plan.json
  snapshots/
    <snapshot_id>/
      manifest.json
      files/
results/
  index.json
  round_NNN/
    manifest.json
    artifacts/
    notebooks/
    source/
```

The import plan is reviewable intent. The snapshot manifest is evidence that the
declared bytes were verified and copied.

Snapshot payloads are marked `-text` in `.gitattributes`, so Git never changes
line endings and invalidates byte-level hashes on checkout.

Every file must belong to exactly one dataset record. Dataset metadata records:

- raw or curated stage;
- provider and licence;
- frequency and units;
- vintage and publication-lag convention;
- missingness policy;
- causal-use restriction;
- transformation lineage.

## Snapshot states

- `provisional`: useful for platform work but not final round evidence;
- `final`: named by a closed round's registration or completion record.

Promotion never mutates a provisional manifest. If the bytes are final, create a
final manifest referring to the same hashes; if any byte changed, import a new
snapshot identifier.

## R15 candidate snapshot

The current provisional snapshot contains 29 files:

- six engine panel files pinned by R15;
- `state_daily.csv`;
- `macro_daily.csv`;
- the byte-pinned `fred_r15` source bundle and its manifest.

It excludes old lab arrays, notebook data, extraction scripts, caches, unused
external panels, and historical intermediate files. R15 is unfinished, so its
final completion record must confirm or replace this snapshot.
