#!/usr/bin/env python3
import argparse, json
from pathlib import Path


def assess(run):
    issues = []
    if not run["vm_reachable"]:
        issues.append("VM endpoint unreachable")
    if run["disk_hash_before"] != run["disk_hash_after"]:
        issues.append("filesystem diverged from checkpoint")
    if run["agent_pid_before"] == run["agent_pid_after"] and run["interrupted_at"] == "boot_agent":
        issues.append("stale agent PID reused")
    if run["checkpoint_age_s"] > 120:
        issues.append(f"checkpoint is stale ({run['checkpoint_age_s']}s)")
    recovered = not issues and run["agent_status"] == "running"
    if recovered:
        action = "none — session is safe to continue"
    elif not run["vm_reachable"]:
        action = "director vm restart --from latest"
    elif run["disk_hash_before"] != run["disk_hash_after"]:
        action = "director snapshot restore --verify"
    else:
        action = "director agent resume --clean"
    return recovered, issues, action


def main():
    parser = argparse.ArgumentParser(description="Recovery preflight for persistent coding-agent VMs")
    parser.add_argument("--input", default="scenarios.json")
    args = parser.parse_args()
    runs = json.loads(Path(args.input).read_text())

    print("MACHINE0 RECOVERY PREFLIGHT")
    print("=" * 72)
    passed = 0
    for run in runs:
        recovered, issues, action = assess(run)
        label = "PASS" if recovered else "REVIEW"
        passed += int(recovered)
        print(f"{label:6} {run['id']:18} interrupted={run['interrupted_at']:13} snapshot={run['snapshot_id']}")
        print(f"       recovery: {run['recovery_time_s']:>3}s | agent={run['agent_status']} | endpoint={'up' if run['vm_reachable'] else 'down'}")
        if issues:
            print("       issues: " + "; ".join(issues))
        print("       next:   " + action)
        print()
    print(f"SUMMARY {passed}/{len(runs)} scenarios recovered cleanly")
    print("Product signal: surface one deterministic next command for every failed state.")


if __name__ == "__main__":
    main()
