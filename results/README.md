# Result evidence status

The two CSV files in this directory are literal transcriptions of manuscript
summary tables. They are retained for traceability and figure regeneration,
not as registered row-level evidence. Their filenames contain `snapshot` and
the integrity validator reports them as `UNVERIFIED_SNAPSHOT_NOT_VALIDATED`.

Do not merge these files into a Primary or TS2Vec ledger. A valid result ledger
must contain unique dataset/method/seed keys, integer correct and test counts,
finite metrics, exact accuracy fractions, and the frozen identity fields.
