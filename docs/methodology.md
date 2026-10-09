# Methodology

This project is designed around a disciplined decision-tree research workflow for a mandate-aware portfolio model.

## Scientific invariants

The platform keeps the following invariants explicit:

- use a single, shared decision and evaluation clock
- apply the same cost model to all arms
- enforce feasibility before reporting weights or exposures
- keep state recognition separate from portfolio action
- do not permit training labels to leak into the held-out read
- record provenance for code, data, and environment

## Round design

Every round should be expressed through a single registration contract:

- objective
- data and snapshot hash
- training and held-out schedule
- model configuration
- constraints
- output schema
- artifact list
- provenance requirements

## Legacy import treatment

A recovered round is not a new design. It is imported as evidence under a neutral contract. The new platform should preserve the original meaning while cleaning the operational boundary.

## Decision rule

The new project should only evolve by adding platform infrastructure or by validating new designs. It should not silently widen scope by carrying historical experiments as active code.
