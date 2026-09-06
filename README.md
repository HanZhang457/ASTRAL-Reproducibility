# ASTRAL reproducibility package

This package rebuilds the computational companion for:

**ASTRAL: Auditable Structural Teacher Representation and Alignment Learning
for Time-Series Classification**

Public repository:
https://github.com/HanZhang457/ASTRAL-Reproducibility

## Important status

The reference implementation and validation framework are reconstructed from
the frozen manuscript specification. Historical result ledgers that could not
be recovered are not fabricated. The nine exact official archive downloads are
included with source URLs, archive hashes, split-file hashes, and observed split
identities. See STATUS_FAIL_CLOSED.md before using any numerical claim.

## Contents

- configs/: frozen paper configuration.
- src/astral/: deterministic teacher, exact kernel realization, neural
  primitives, fusion, data loading, and audit utilities.
- scripts/: data retrieval, validation, exact ASTRAL-K execution, figures, and
  end-to-end orchestration.
- tests/: finite-dimensional implementation tests.
- results/: manuscript snapshots, explicitly marked unverified.
- validation/: expected historical hashes and generated receipts.
- paper/: latest recoverable Springer LaTeX source and bibliography.

## Quick start

Create the historical environment:

    conda env create -f environment.yml
    conda activate astral-reproduction
    pip install -e .

Run source-level checks:

    make test
    python scripts/smoke_test.py

The nine downloaded archives and extracted official splits are already under
`data/raw/`. To retrieve fresh copies from the same no-login source:

    python scripts/fetch_datasets.py --keep-archives
    python scripts/validate_datasets.py

Run the exact ASTRAL-K path on one dataset:

    python scripts/run_exact_astral.py GunPoint

Rebuild available outputs and validation receipts:

    python scripts/reproduce_all.py
    python scripts/verify_integrity.py
    python scripts/build_manifest.py

Build the Springer Nature manuscript:

    make paper

Use "--strict" with verify_integrity.py only after the historical frozen
artifacts have been placed at the paths in validation/EXPECTED_SHA256SUMS.txt.

## Reproduction boundaries

The exact teacher and kernel path can be reproduced with NumPy, SciPy, and
scikit-learn. The neural path requires PyTorch. Random-convolution baselines
require aeon. TS2Vec requires its separately pinned implementation and is not
silently replaced by another encoder.

No test labels are used to construct descriptors, calibrate component
bandwidths, train representations, or choose epochs. Duplicate experimental
keys, nonfinite values, and inconsistent correct/test fractions are rejected.

## One-location review route

Reviewers can clone the public repository, install the locked environment, run
`python scripts/validate_datasets.py`, then run `make test`, `make verify`, and
`make paper`. The included exact data archives remove the need for a second
login or data portal during reproduction.
