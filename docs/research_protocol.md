# Research protocol

This repository follows a strict protocol for round execution and evidence handling.

## Lifecycle

### 1. Registration
A round starts with a formal specification. The specification defines the research question, the train/hold-out schedule, the data snapshot, the model structure, the constraints, and the artifact list.

### 2. Pre-flight validation
Before execution, validate:

- required files exist
- hashes match the expected snapshot
- configuration is internally coherent
- constraints are feasible
- output directories are set up
- provenance requirements are active

### 3. Execution
The experiment runs in a controlled environment. All generated results are written through the round's artifact contract.

### 4. Artifact capture
Every artifact must be recorded as part of the round manifest, with path and hash.

### 5. Hold-out read
The held-out result is the only result that determines the scientific read. It must be clearly separated from training-side tuning.

### 6. Indexing
The round is registered in the project index and all artifact metadata is assembled into a clean catalog.

### 7. Presentation
Only a presentation notebook or summary report should read the result index. It should not regenerate the research itself.

## Legacy recovery

A recovered legacy round must be treated as imported evidence. It must be captured as a neutral round with provenance and an import manifest. It must never be mistaken for a fresh round implementation.
