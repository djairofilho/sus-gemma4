# Evals

Deterministic regression checks for SUS workflow behavior, schema validity, and safety constraints.

The initial eval runner uses the local mock triage service so it can run in CI without Ollama, network access, or patient data.

## Run

```bash
python evals/scripts/run_safety_evals.py
```

Optional live Ollama evals are disabled unless explicitly requested:

```bash
GEMMA_SUS_RUN_LIVE_OLLAMA_EVALS=true python -m evals.scripts.run_live_ollama_evals
```

The live runner uses local Ollama settings from `GEMMA_SUS_OLLAMA_BASE_URL`, `GEMMA_SUS_OLLAMA_MODEL`, and `GEMMA_SUS_OLLAMA_TIMEOUT_SECONDS`.

## Data Rules

- Use synthetic or anonymized cases only.
- Do not include real patient names, identifiers, phone numbers, addresses, or dates of birth.
- Prefer property-based expectations over exact prose comparisons.
