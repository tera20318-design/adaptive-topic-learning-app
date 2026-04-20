# Domain Adapter Schema

This markdown schema is the human-readable contract for the per-run domain adapter.
The machine-readable companion is [domain-adapter.schema.json](./domain-adapter.schema.json).

## Rule

The adapter is generated fresh for each run from the current topic, reader, use context, risk tier, and evidence plan.
It must not copy a stored risk list from a prior topic.

## Required Fields

| field | type | required | meaning |
| --- | --- | --- | --- |
| `topic` | string | yes | current run topic |
| `reader` | string | yes | intended reader |
| `use_context` | string | yes | why the reader needs the report |
| `output_type` | string | yes | intended reader-facing output form |
| `risk_tier` | `low|medium|high` | yes | run-level risk tier |
| `temporal_sensitivity` | `low|medium|high` | yes | how date-sensitive the topic is |
| `jurisdiction_sensitivity` | `low|medium|high` | yes | how scope changes across jurisdictions |
| `source_priority` | list[`source_role`] | yes | retrieval and ranking order |
| `high_risk_claim_types` | list[`claim_kind`] | yes | claim kinds that trigger stricter support rules |
| `likely_failure_modes` | list[string] | yes | topic-shaped failure risks generated for this run |
| `domain_specific_risks` | list[string] | yes | per-topic risk inventory generated fresh |
| `common_misunderstandings` | list[string] | yes | likely reader confusions |
| `boundary_concepts` | list[string] | yes | concepts that separate adjacent subjects |
| `decision_context` | object | yes | what the reader is deciding and under what constraints |
| `required_decision_layer` | list[string] | yes | what the report must help the reader decide next |
| `required_tables` | list[string] | yes | tables or checklists required by the adapter |
| `must_not_overgeneralize` | list[string] | yes | overclaim boundaries to keep visible |
| `known_limits` | list[string] | yes | limits already known at planning time |
| `source_roles_required_by_claim_kind` | map[`claim_kind` -> list[`source_role`]] | yes | claim-level source-role requirements for this run |

## `decision_context` Fields

| field | type | required | meaning |
| --- | --- | --- | --- |
| `primary_decision` | string | yes | main decision or judgment the report supports |
| `failure_cost` | `low|medium|high` | yes | consequence of getting the decision wrong |
| `time_horizon` | string | yes | relevant decision horizon |
| `reader_action` | string | yes | likely next action after reading |

## Generation Constraints

- `domain_specific_risks` must be generated from the current run, not copied from a fixture list.
- `required_tables` must be derived from output purpose and decision context, not from remembered topic templates.
- `must_not_overgeneralize` must express scope boundaries, not named historical incidents.
- `source_roles_required_by_claim_kind` must be compatible with the core claim-kind/source-role matrix.

## Failure Handling

If any required field is missing or still generic filler, the adapter is incomplete.
An incomplete adapter should prevent downstream report planning from claiming readiness.
