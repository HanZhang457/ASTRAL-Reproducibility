# ASTRAL Reproducibility Repository

Public computational companion for:

> **ASTRAL: Auditable Structural Teacher Representation and Alignment Learning for Time-Series Classification**

**Release status: PRE-RELEASE.** Public access is active, but this repository must not yet be cited as complete replication evidence. The scientific release becomes valid only after every item in [RELEASE_GATES.md](RELEASE_GATES.md) passes and an immutable `v1.0.0` release is issued.

## Purpose

This repository is designed as the single, no-login location for the manuscript's:

- executable reference implementation;
- exact data and official train/test split identities;
- frozen configurations, seeds, and dependency locks;
- row-level experimental results;
- table and figure generation scripts;
- integrity receipts and clean-environment reproduction report.

Recovery checkpoints are retained only as recovery evidence. They are not promoted to registered experimental results.

## Planned repository layout

```text
configs/        frozen experiment and method configurations
data/           exact inputs, split manifests, checksums, and provenance
src/            ASTRAL reference implementation
scripts/        validation and end-to-end reproduction entry points
results/        row-level registered results and summary outputs
figures/        deterministic figure-generation sources and outputs
validation/     integrity, identity, and clean-reproduction receipts
paper/          manuscript source corresponding to the released evidence
```

## Integrity anchors

The release process is fail-closed: a file is accepted only when its byte identity matches the frozen record.

| Object | Expected SHA-256 |
|---|---|
| Formal 1,099-row checkpoint package | `f91c6e3581793acf8ccefb394eb16dd048e42f181078f0c63dd0972be88e8e41` |
| InsectWingbeat context cache | `460c0f6c4dab7ecbb20e7912ec3330e32cfc0038732afa219ac51a936d9a53d8` |
| Frozen InsectWingbeat TRAIN split | `40ec78dc13be1df92590535aeab8e724d8efda1c5d9fe33ed03ce9614675bb2e` |
| Frozen InsectWingbeat TEST split | `aee200865239737b9304e80949153f5193cac3d08b98dac9ced8ddf1f1189f89` |
| CONTEXT 150/150 recovery archive | `4fe3998758b73b1dc9f3ffad610db664a9eeca0648fd58f9610be73d3298fcbe` |

## Naming continuity

The manuscript name **ASTRAL** replaces the historical working name **TASSL**. Historical filenames and experiment identifiers remain unchanged where required for checksum continuity. The mapping is one-to-one and does not change models, hyperparameters, seeds, splits, predictions, or statistical rules.

## Access

This repository is public and can be opened without a GitHub account:

<https://github.com/HanZhang457/ASTRAL-Reproducibility>

A permanent archival DOI will be added after the complete, verified `v1.0.0` release is deposited in an archival service.

## Citation

Citation metadata will be added only after the complete evidence release is signed.
