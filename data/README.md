# Data and split provenance

The signed release will place the manuscript's exact computational inputs in this directory, subject to the original archive redistribution terms.

## Dataset panel

- ItalyPowerDemand
- GunPoint
- ArrowHead
- BasicMotions
- ECG200
- Coffee
- Epilepsy
- AtrialFibrillation
- StandWalkJump
- InsectWingbeat (completion and recovery audit)

Official UCR/UEA train/test boundaries are preserved. No random resplitting of the official test sets is permitted.

## Acceptance rule

A dataset becomes release-valid only when:

1. the exact file is present or a lawful, immutable mirror is supplied;
2. its SHA-256 matches the frozen manifest;
3. shape, label set, train/test counts, and split identifier pass validation;
4. no test label is used for descriptor calibration, representation training, epoch selection, or model selection.

Files not meeting all four conditions remain blocked and cannot support a manuscript claim.
