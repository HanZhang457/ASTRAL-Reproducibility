# Public Release Gates

The repository follows a fail-closed release policy. A checked box requires a stored, inspectable receipt; an unchecked box blocks the complete-reproduction claim.

| Gate | Requirement | Status |
|---|---|---|
| R1 Public access | Repository opens without login | PASS |
| R2 Source identity | Complete executable source and five frozen source hashes match | BLOCKED |
| R3 Exact data | Exact data/splits are present or mirrored lawfully; SHA-256 identities match | BLOCKED |
| R4 Environment | Frozen dependency files install cleanly and dependency audit passes | BLOCKED |
| R5 Experimental grid | Expected keys are complete and unique; duplicates are rejected | BLOCKED |
| R6 Numerical integrity | All stored metrics are finite and integer-count consistency passes | BLOCKED |
| R7 Reproduction | One-command clean run regenerates registered tables and figures | BLOCKED |
| R8 Manuscript alignment | Numerical claims, tables, figures, source, and repository agree | BLOCKED |
| R9 Immutable archive | Tagged release and permanent archival DOI are public | BLOCKED |

## Release rule

The repository may be described as **publicly accessible** now. It must not be described as **complete**, **cleanly reproducible**, or **permanently archived** until R1–R9 all pass.

## Required top-level commands for the signed release

The final release will provide:

```bash
python scripts/verify_integrity.py
python scripts/reproduce_registered_results.py
python scripts/reproduce_tables.py
python scripts/reproduce_figures.py
```

A platform-neutral wrapper and exact expected outputs will accompany these commands.
