# Cosmic-1 Edge-Case Replay Queue

A small, dependency-free demo that turns field-deployment attempts into a prioritized queue for replay, retraining, and regression testing.

## Why this matters

A general-purpose robotic platform learns fastest when failed attempts and operator corrections become structured engineering signals instead of isolated video clips. This demo groups runs by likely failure mode and ranks the clips with the highest learning value.

Signals used:

- perception confidence
- grasp-pose offset
- workpiece deflection
- operator intervention
- task outcome

## Run

```bash
python demo.py --input attempts.csv
```

No packages are required beyond Python 3.10+.

## Example output

```text
LOW_PERCEPTION_CONFIDENCE    runs=3 failures=3 peak_value=7.48
GRASP_POSE_DRIFT             runs=2 failures=2 peak_value=7.32
WORKPIECE_DEFLECTION         runs=1 failures=1 peak_value=4.44

TOP CLIPS FOR RETRAINING / REGRESSION
1. siteC-003 score=7.48 LOW_PERCEPTION_CONFIDENCE
2. siteB-041 score=7.32 GRASP_POSE_DRIFT
3. siteD-002 score=7.13 LOW_PERCEPTION_CONFIDENCE
```

## Product extension

The same pipeline could ingest real telemetry and clip metadata, attach the operator correction, and export a replay manifest for simulation plus a fixed regression set for the next policy release.

Built as a focused proof of work for Cosmic Robotics.
