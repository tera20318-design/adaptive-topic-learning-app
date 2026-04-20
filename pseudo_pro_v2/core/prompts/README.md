# Prompt Contracts

Core prompts may contain:

- abstract task descriptions for each stage
- schema references
- claim-kind and source-role definitions
- risk-tier and scope semantics
- report-first writing rules
- absence and contradiction handling rules

Core prompts may not contain:

- named substances
- named products
- named standards
- named regulations
- named countries or authorities as permanent defaults
- language copied from a regression fixture
- concrete must-cover angles taken from a historical run

Fixture-specific wording belongs in `fixtures/`.

