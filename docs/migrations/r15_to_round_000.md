# R15 to Round 000 recovery

R15 is unfinished. This document defines what can be prepared now and what is
strictly blocked until R15 closes.

## Current state

- Round 000 is reserved.
- Its manifest status is `awaiting_source_completion`.
- No R15 output has been imported.
- Notebook generation must fail while the round is pending.

## Work allowed before R15 closes

- define schemas and validators;
- classify candidate capabilities;
- test recovery refusal and path safety;
- define the source-completion record;
- improve the new repository's architecture and documentation;
- design round-agnostic interfaces without claiming R15 behavior is final.

## Work prohibited before R15 closes

- copying provisional R15 results;
- describing a provisional verdict as Round 000;
- selecting migration candidates because an unfinished result looks favorable;
- freezing R15 configuration or documentation as final;
- generating a Round 000 results notebook;
- implementing native execution around temporary R15 phase scripts.

## Source closure package

After R15 closes, create one JSON completion record conforming to
`config/schemas/source-completion.schema.json`. It must contain:

- the final source and superproject revisions;
- accurate worktree dirtiness and diff hash;
- the final source-round status;
- every artifact selected for recovery;
- source and target paths;
- SHA-256 for every artifact;
- a neutral description of every artifact.

Start from `config/recovery/r15_completion_inventory.template.json`. Set
`source_complete` only after formal closure, enumerate the selected artifacts,
then run:

```powershell
dtm create-completion-record `
  --source-root C:\path\to\kiss_etf_optimizer `
  --inventory C:\path\to\r15_completion_inventory.json `
  --output C:\path\to\r15_source_completion.json
```

Review the dry-run result, then repeat with `--execute` and
`--confirm-source-complete`.

The artifact list must include, when they exist:

1. final resolved R15 registration and amendments;
2. final source code provenance and environment manifest;
3. input-data manifest and hashes, not uncontrolled raw duplicates;
4. frozen model/state/action objects required to audit the result;
5. split-level held-out predictions, returns, and portfolio paths;
6. evaluation distributions and point-estimate reconciliation;
7. final result summary and decision record;
8. the minimal source documentation needed to interpret those artifacts.

For D9, the inventory should also capture the final per-split base-band choice,
common-reference member scores, mandate restoration audit, seam-block records,
nested eligibility, placebo recomputation, held-out access proof, average-book
projection result, point-estimate reconciliation, D7/D8 verification, timing
stop, and deployed-object verification when those artifacts exist.

Search logs, temporary checkpoints, caches, failed-run output, and presentation
duplicates are excluded unless the final audit explicitly depends on them.

## Recovery procedure

1. Close R15 in the source repository.
2. Commit coherent source and final records.
3. Record the source submodule and superproject revisions.
4. Build the completion record without modifying this repository's pending round.
5. Run `dtm recover-legacy` without `--execute`.
6. Review the verified artifact inventory and target paths.
7. Run the same command with `--execute`.
8. Validate Round 000 and rebuild the project index.
9. Generate the presentation notebook from the recovered manifest.
10. Compare the notebook and indexed metrics to the source artifacts.
11. Commit the recovered round as one auditable change.

## Acceptance criteria

- all copied bytes match their declared source hashes;
- every target path is inside `results/round_000/`;
- the manifest is the final write and validates as `recovered`;
- the result index is reproducible from manifests;
- the notebook reads only recovered artifacts;
- no old source module is required merely to inspect Round 000;
- imported evidence is distinguishable from any later reproduction.
