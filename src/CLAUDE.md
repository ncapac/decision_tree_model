# Source rules

- Keep reusable implementation under `decision_tree_model`.
- No module, class, or function name may encode a round number.
- Package code must not know the old repository's filesystem layout.
- Workflows receive paths and manifests as inputs; they do not discover legacy
  files by convention.
- Raise explicit errors for missing, inconsistent, or unverified evidence.
- Keep CLI parsing in `decision_tree_model.cli`; keep testable behavior in
  package workflows and domain modules.
