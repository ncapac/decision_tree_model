# Architecture

This project separates reusable platform code from round-specific evidence.

## Layers

### 1. Project configuration
The configuration layer defines the active project defaults, the default round, the artifact root, and the validation requirements. It must not include historical round logic.

### 2. Round lifecycle
Each round is a bounded workflow:

1. registration
2. data validation
3. execution
4. artifact persistence
5. provenance capture
6. round index update
7. presentation summary

### 3. Shared platform code
Reusable code lives under `src/decision_tree_model/` and should not depend on a specific round number or legacy artifact layout.

### 4. Legacy import workflow
Legacy imports happen through a dedicated neutral process. Imported rounds stay immutable and are normalized to a new round contract.

## Dependency direction

Project config -> round config -> workflow -> shared platform -> artifact manifest

Shared code does not read round-specific files directly. Round-specific data is supplied via manifests and validated configuration.

## Design rule

The project should remain small. If a helper is only needed for one round, it should be kept in that round's folder or moved to a reusable package only after it becomes genuinely general.
