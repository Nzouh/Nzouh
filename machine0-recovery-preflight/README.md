# machine0 Recovery Preflight

A small, dependency-free demo for testing whether a persistent coding-agent VM can recover safely after provisioning, checkpoint, endpoint, or resume failures.

## Why this matters

Long-running coding agents turn recovery behavior into product behavior. A failed restore should not leave the user guessing whether the filesystem is consistent, whether the endpoint is alive, or which command to run next.

This demo checks:

- endpoint reachability
- checkpoint freshness
- filesystem consistency
- agent-process state
- recovery time

It then emits one clear next action for every failed scenario.

## Run

```bash
python demo.py --input scenarios.json
```

No packages are required beyond Python 3.10+.

## Example output

```text
PASS   long-task-resume   interrupted=checkpoint    snapshot=snap-0192
       recovery: 19s | agent=running | endpoint=up
       next: none — session is safe to continue

REVIEW volume-attach-cut  interrupted=attach_volume snapshot=snap-0187
       issues: filesystem diverged from checkpoint
       next: director snapshot restore --verify

REVIEW endpoint-loss      interrupted=allocate_vm   snapshot=snap-0181
       issues: VM endpoint unreachable
       next: director vm restart --from latest
```

## Product extension

The same evaluator could sit behind a CLI command such as `director recover --explain`, ingest real provisioning events, and return both a machine-readable verdict and a user-facing recovery command.

Built as a focused proof of work for machine0.
