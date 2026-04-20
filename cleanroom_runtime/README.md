# Cleanroom Runtime

`cleanroom_runtime` is a from-scratch runtime rebuild for a generic pseudo-Pro / pseudo-Deep-Research pipeline.

The package keeps the stage-based architecture and schema-level separation from earlier experiments, but it intentionally avoids:

- topic-shaped behavior in core logic
- self-confirming metrics
- treating claim capture as claim support
- allowing unsupported high-risk claims to disappear from audit outputs
- presenting synthetic validation as research completeness

Package layout:

```text
cleanroom_runtime/
  README.md
  migration-note.md
  src/
    cleanroom_runtime/
      catalogs.py
      models.py
      pipeline.py
      utils.py
      validators.py
      stages/
        *.py
  tests/
    *.py
```

The core package is intentionally generic. Synthetic fixtures belong in tests only.
