# research-os-v2 fixtures

These fixtures are clean-room regression inputs for pseudo-Pro v2 behavior.

Each fixture JSON should include the same top-level shape:

- `topic`
- `reader`
- `use_context`
- `output_type`
- `requested_mode`
- `expected_domain_adapter_traits`
- `known_failure_modes`
- `required_source_roles`
- `required_claims`
- `prohibited_overclaims`
- `expected_gate_behavior`
- `source_packets`

`expected_gate_behavior` should stay within the allowed set used by the regression test.
The current suite uses `allow`, `review`, and `block`.

`source_packets` are structured source records. Each packet should include:

- `source_id`
- `title`
- `source_role`
- `published_on`
- `jurisdiction`
- `quality_flags`
- `summary`
- `findings`

Each finding should include:

- `finding_id`
- `statement`
- `claim_kind`
- `risk_level`
- `section_hint`
- `decision_note`
- `risk_tags`
- `failure_modes`
- `misunderstandings`
- `boundary_concepts`
- `confidence`
- `support_status_hint`

High-stakes fixtures should require at least one `authoritative` source role.
