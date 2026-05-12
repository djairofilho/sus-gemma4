#!/usr/bin/env sh
set -eu

MAX_ITERATIONS="${RALPH_MAX_ITERATIONS:-5}"
ITERATION=1

printf '%s\n' "ralph: start max_iterations=$MAX_ITERATIONS"

while [ "$ITERATION" -le "$MAX_ITERATIONS" ]; do
  printf '%s\n' "ralph: iteration $ITERATION"

  if sh scripts/validate.sh; then
    printf '%s\n' "ralph: validation passed"
    exit 0
  fi

  printf '%s\n' "ralph: validation failed"
  printf '%s\n' "ralph: hand off to an agent with prompts/ralph-loop.md, then rerun this script"

  if [ "${RALPH_NON_INTERACTIVE:-0}" = "1" ]; then
    exit 1
  fi

  ITERATION=$((ITERATION + 1))
  break
done

printf '%s\n' "ralph: stopped before validation passed"
exit 1
