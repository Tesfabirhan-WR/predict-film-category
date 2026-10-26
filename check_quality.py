"""Quality gate: exits with code 1 if metrics.json does not meet the thresholds of config.yaml.

Usage:
    python check_quality.py
    python check_quality.py --metrics tests/fake_model/metrics.json   # must FAIL
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config.yaml"
DEFAULT_METRICS = ROOT / "model" / "metrics.json"


def load_config(path=DEFAULT_CONFIG):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_metrics(path=DEFAULT_METRICS):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check(metrics, config):
    """Return the list of problems (empty list = model accepted)."""
    problems = [f"missing key in metrics.json: {key}" for key in ("f1_test", "test_size") if key not in metrics]
    if problems:
        return problems

    if metrics["f1_test"] < config["min_f1"]:
        problems.append(f"test F1 {metrics['f1_test']:.3f} is below the minimum {config['min_f1']:.3f}")
    if metrics["test_size"] < config["min_test_size"]:
        problems.append(f"test size {metrics['test_size']} is below the minimum {config['min_test_size']}")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--metrics", default=DEFAULT_METRICS, type=Path)
    parser.add_argument("--config", default=DEFAULT_CONFIG, type=Path)
    args = parser.parse_args(argv)

    metrics = load_metrics(args.metrics)
    config = load_config(args.config)
    problems = check(metrics, config)

    if problems:
        print("QUALITY GATE FAILED")
        for problem in problems:
            print(f" - {problem}")
        return 1

    print(f"QUALITY GATE PASSED: F1 = {metrics['f1_test']:.3f} (min {config['min_f1']:.3f}), "
          f"test size = {metrics['test_size']} (min {config['min_test_size']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
