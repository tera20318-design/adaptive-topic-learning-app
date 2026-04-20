# Domain Adapter

- topic: User document review of employee fertility travel reimbursement memo
- reader: HR operations
- use_context: Review the uploaded policy before HR tells employees today that the memo legally covers every medical travel reimbursement scenario
- risk_tier: high
- source_priority: official_regulator, legal_text, court_or_authoritative_interpretation, academic_review, professional_body, government_context
- high_risk_claim_types: absence, financial, legal, medical, regulatory
- likely_failure_modes: Claim support inferred from generic authority instead of claim-kind requirements., Scoped absence rewritten as a settled fact., Repeated findings used to make the bundle look richer than the evidence is.
- common_misunderstandings: Claim capture is not the same thing as claim support., Scoped absence does not prove global absence., Synthetic validation does not imply live research completeness.
- boundary_concepts: evidence vs inference, scoped absence vs settled fact, contract completeness vs research completeness
- required_tables: Verification checklist, Document grounding checklist
