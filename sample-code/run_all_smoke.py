#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def run_one(py: str, script: Path) -> bool:
    print(f"\n=== RUN {script.name} ===")
    proc = subprocess.run([py, str(script)], capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip())
    print(f"exit={proc.returncode}")
    return proc.returncode == 0


def main() -> None:
    py = sys.executable
    base = Path(__file__).parent
    scripts = [
        base / "linear_algebra_example.py",
        base / "deep_learning_example.py",
        base / "training_flow_example.py",
        base / "inference_flow_example.py",
        base / "attention_example.py",
    ]

    ok_all = True
    for script in scripts:
        ok_all = run_one(py, script) and ok_all

    print("\n=== SUMMARY ===")
    print("PASS" if ok_all else "FAIL")
    raise SystemExit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
