from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from app.config import get_settings
from app.ollama_client import OllamaClient
from app.services.triage import create_triage_response
from evals.scripts.run_safety_evals import (
    DEFAULT_CASES_PATH,
    SafetyEvalCase,
    SafetyEvalFailure,
    evaluate_response,
    format_failures,
    load_cases,
)

LIVE_EVAL_ENV = "GEMMA_SUS_RUN_LIVE_OLLAMA_EVALS"


def live_evals_enabled(environ: dict[str, str] | None = None) -> bool:
    values = os.environ if environ is None else environ
    return values.get(LIVE_EVAL_ENV, "").lower() == "true"


async def run_live_cases(cases: list[SafetyEvalCase]) -> list[SafetyEvalFailure]:
    settings = get_settings()
    runtime = OllamaClient(
        settings.ollama_base_url,
        settings.ollama_model,
        settings.ollama_timeout_seconds,
    )
    failures: list[SafetyEvalFailure] = []

    for case in cases:
        response = await create_triage_response(case.input, runtime)
        failures.extend(evaluate_response(case, response))

    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run opt-in live Ollama SUS safety evals.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    return parser.parse_args()


def main() -> int:
    if not live_evals_enabled():
        print(f"skip live Ollama evals: set {LIVE_EVAL_ENV}=true to run")
        return 0

    args = parse_args()
    cases = load_cases(args.cases)
    failures = asyncio.run(run_live_cases(cases))

    if failures:
        print("Live Ollama eval failures:")
        print(format_failures(failures))
        return 1

    print(f"Live Ollama evals passed: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
