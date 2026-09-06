# Exact data policy

The paper uses the official predefined UCR/UEA train/test files listed in
datasets.yaml. Run "python scripts/fetch_datasets.py" to place the archive
files under data/raw/ and record their downloaded SHA-256 values.

The package contains the nine archives downloaded from the no-login archive
URLs in `datasets.yaml`, plus their extracted official TRAIN/TEST files.
`raw/DOWNLOAD_RECEIPT.json` records archive SHA-256 values and
`../validation/dataset_receipt.json` records exact split-file SHA-256 values,
sizes, shapes, and class counts. Preserve upstream attribution and confirm
redistribution terms before publishing the copied archive bytes elsewhere.
