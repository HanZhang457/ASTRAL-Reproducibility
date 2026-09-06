# ASTRAL package validation report

Validation date: 2026-09-06

| Gate | Status | Evidence |
|---|---|---|
| Reference implementation | PASS | Six unit tests and deterministic smoke test |
| Kernel/fingerprint invariants | PASS | Symmetry, PSD tolerance, nonnegativity, unit-sum fingerprints |
| Exact kernel coordinates | PASS | Training and out-of-sample coordinate agreement |
| Input data availability | PASS | Nine no-login archives included under `data/raw/` |
| Split identity | PASS | 9/9 TRAIN/TEST counts, lengths, channels, and classes match |
| Data integrity | PASS | Archive CRC/SHA-256 and split-file SHA-256 receipts |
| Figures | PASS | 4/4 generated; Figures 1--2 editable TikZ, Figures 3--4 Matplotlib |
| Manuscript build | PASS | 23-page PDF; no missing figure, undefined citation/reference, or fatal error |
| Historical Primary ledger | BLOCKED | Original 1,099-row file not recovered |
| Registered InsectWingbeat 7/7 | BLOCKED | Recovery state cannot replace registered rows |
| TS2Vec 158/158 | BLOCKED | Original row-level ledger not recovered |
| Numerical table reproduction | BLOCKED | Summary CSVs are transcriptions, not registered evidence |

The package therefore passes source, data-access, split-identity, figure, and
manuscript-build gates. It does not certify the manuscript's historical
numerical tables. Those claims remain fail-closed until exact ledgers are
restored or all frozen experiments are rerun.
