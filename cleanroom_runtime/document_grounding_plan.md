## Document Grounding V3

### Goal

Document grounding v3 strengthens the live-lite path for user-provided text by preserving an inspectable chain across:

1. checked raw document text
2. grounded finding spans
3. claim ledger linkage
4. citation ledger linkage
5. final prose span linkage

The runtime still proves what the checked document says directly. It does not treat an uploaded document as topic-wide authority.

### Supported modes

- `excerpt`
  - keeps the old bounded excerpt path
  - suitable for short checked snippets
- `document_review`
  - treats multi-paragraph checked text as review material
  - keeps checked blocks separate
  - does not allow cross-block synthesis to clear support

### Implemented path

1. `RawDocumentInput` accepts raw text or markdown-like excerpt content plus `review_mode`.
2. `document_packets_from_raw_documents(...)` converts the raw document into a normalized `SourcePacket`.
3. Each grounded finding keeps:
   - direct excerpt text
   - source span labels and offsets
   - grounding marker
   - grounding scope note
4. Evidence ingestion preserves those fields instead of flattening them away.
5. Claim and citation ledgers now retain:
   - claim span offsets
   - claim-to-finding linkage
   - finding-to-source excerpt linkage
   - multispan source offsets
   - scope-limiting grounding notes

### Guardrails

- Direct grounding must remain visibly limited to the checked document text.
- Separate checked blocks remain separate evidence units.
- Multi-span support is allowed only inside one checked block.
- Unsupported synthesis across separate blocks degrades support and traceability.
- Summary prose must not outrun grounded spans.
- High-risk document-backed prose without inspectable spans cannot clear release.
- Direct grounding does not imply authoritative support.
- Out-of-scope extrapolation is disallowed.

### What is now proven

The runtime can now show an inspectable chain from checked document text to grounded finding spans, then into claim and citation ledgers, then into final prose units.

Synthetic document grounding can prove the contract path, but it does not prove external corroboration or real-world completeness.

### Remaining boundary

- No OCR
- No PDF parser
- No cross-document merge into one supported claim
- No semantic grounding without checked spans
- No external corroboration from live retrieval

### Remaining runtime work

- parser-mediated document extraction
- cross-document reconciliation that still preserves inspectable span lineage
- live corroboration beyond the checked document boundary
