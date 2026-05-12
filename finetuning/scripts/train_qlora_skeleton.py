from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "finetuning" / "datasets" / "seed.jsonl"
DEFAULT_OUTPUT_DIR = ROOT / "finetuning" / "adapters" / "gemma-sus-qlora"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Skeleton entrypoint for future Unsloth QLoRA runs.")
    parser.add_argument("--model", default="gemma-4-local-placeholder")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("QLoRA skeleton only; no training is executed by default.")
    print(f"model={args.model}")
    print(f"dataset={args.dataset}")
    print(f"output_dir={args.output_dir}")
    print("Install Unsloth and add reviewed training parameters before running real training.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
