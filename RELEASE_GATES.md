# ASTRAL release gates

This release separates reproducible reference-code validation from historical
experimental-evidence validation. A gate marked **BLOCKED** cannot be promoted
to PASS by rerunning the reference implementation.

| Gate | Status | Evidence |
|---|---|---|
| Source import and unit tests | PASS | Six deterministic unit tests plus the smoke test |
| Exact public archive splits | PASS | Nine downloaded UCR/UEA archives; ZIP CRC and split digests recorded |
| Deterministic exact-path rebuild | PASS | Nine fresh ASTRAL-K rows in `results/rebuilt_exact.csv` |
| Duplicate-key rejection and atomic writes | PASS | Enforced by `scripts/run_exact_astral.py` |
| Manuscript build | PASS | `pdflatex`/BibTeX build, 35 bibliography items, four vector/raster figures |
| Historical Primary ledger (1,106/1,106) | BLOCKED | The registered 1,099-row bundle and seven InsectWingbeat rows are unavailable |
| Historical TS2Vec ledger (158/158) | BLOCKED | Registered row-level ledger is unavailable |
| Historical manuscript-number reproduction | BLOCKED | Snapshot tables are retained as unverified manuscript snapshots |

The authoritative machine-readable state is `validation/STATUS.json`. See
`STATUS_FAIL_CLOSED.md` for the exact missing artifact identities.
