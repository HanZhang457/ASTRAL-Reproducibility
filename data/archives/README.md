# Included official archive bytes

The public GitHub copy stores each official ZIP as numbered binary parts so
every object stays small enough for ordinary repository access. Reassemble and
extract them with:

```text
python scripts/extract_included_archives.py
python scripts/validate_datasets.py
```

Part concatenation is byte preserving. The reconstructed archive SHA-256 values
must match `../raw/DOWNLOAD_RECEIPT.json` in the full package.
