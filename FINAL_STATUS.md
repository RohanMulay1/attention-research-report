# Final status

The report is complete when its clean-clone build, rendered-PDF tests, source
traceability tests, and CI all pass. Measurements are regenerated from the two
source repositories when they are present; committed PNGs are checked for
pixel drift.

## Score

Pending final QA and remote CI. A 10/10 score will be recorded only after both
are green.

## Remaining

- CRPA Tier 2 at 32k and 64k awaits the bounded diagnostic GPU run.
- CFG_S and CFG_M await the clean, matched-budget factorial run.
- GPT-2 Check-1 remains unexplained after the full unselected 13-row grid.
- A6 value-residual and register methods remain intentionally not run because
  the former requires matched-capacity training and the latter is a vision
  token intervention outside the causal-LM harness.
