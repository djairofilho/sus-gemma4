# Evals

Deterministic regression checks for SUS workflow behavior, schema validity, and safety constraints.

The initial eval runner uses the local mock triage service so it can run in CI without Ollama, network access, or patient data.

## Run

```bash
python evals/scripts/run_safety_evals.py
```

## Data Rules

- Use synthetic or anonymized cases only.
- Do not include real patient names, identifiers, phone numbers, addresses, or dates of birth.
- Prefer property-based expectations over exact prose comparisons.
