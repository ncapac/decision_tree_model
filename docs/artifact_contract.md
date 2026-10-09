# Artifact contract

This project treats artifacts as governed, machine-readable evidence.

## Required properties

Every artifact must have:

- a round identifier
- a relative path
- a kind or type
- a checksum
- a timestamp
- an owner or source process
- a description

## Required directories

- `results/<round>/manifest.json`
- `results/<round>/artifacts/`
- `results/<round>/notebooks/`
- `results/index.json`

## Reverse lookup policy

The artifact database must be rebuildable from files. It is not allowed to become a hidden source of truth.

## Imported legacy rounds

For imported legacy rounds, the manifest must record:

- original source project
- original round label
- import date
- source path or archive reference
- source hash
- import note
