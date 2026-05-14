#!/usr/bin/env sh
set -eu

log() {
  printf '%s\n' "$1"
}

can_run_command() {
  command_name="$1"
  command -v "$command_name" >/dev/null 2>&1 && "$command_name" --version >/dev/null 2>&1
}

run_if_package_script_exists() {
  project_dir="$1"
  script_name="$2"

  package_json="$project_dir/package.json"

  if [ ! -f "$package_json" ]; then
    log "skip $project_dir $script_name: package.json not found"
    return 0
  fi

  if [ -f "$project_dir/pnpm-lock.yaml" ] && can_run_command pnpm; then
    log "run $project_dir pnpm $script_name"
    (cd "$project_dir" && pnpm run "$script_name" --if-present)
  elif [ -f "$project_dir/yarn.lock" ] && can_run_command yarn; then
    log "run $project_dir yarn $script_name"
    (cd "$project_dir" && yarn run "$script_name" --if-present)
  elif can_run_command npm; then
    log "run $project_dir npm run $script_name"
    (cd "$project_dir" && npm run "$script_name" --if-present)
  else
    log "skip $project_dir $script_name: no supported package manager found"
  fi
}

run_legacy_root_package_script_if_exists() {
  script_name="$1"

  if [ ! -f package.json ]; then
    log "skip $script_name: package.json not found"
    return 0
  fi

  if [ -f pnpm-lock.yaml ] && can_run_command pnpm; then
    log "run pnpm $script_name"
    pnpm run "$script_name" --if-present
  elif [ -f yarn.lock ] && can_run_command yarn; then
    log "run yarn $script_name"
    yarn run "$script_name" --if-present
  elif can_run_command npm; then
    log "run npm run $script_name"
    npm run "$script_name" --if-present
  else
    log "skip $script_name: no supported package manager found"
  fi
}

python_command() {
  if can_run_command python; then
    printf '%s\n' "python"
  elif can_run_command python3; then
    printf '%s\n' "python3"
  elif can_run_command python.exe; then
    printf '%s\n' "python.exe"
  else
    return 1
  fi
}

python_command_with_modules() {
  for candidate in python python3 python.exe; do
    if ! can_run_command "$candidate"; then
      continue
    fi

    has_modules=1
    for module_name in "$@"; do
      if ! "$candidate" -m "$module_name" --version >/dev/null 2>&1; then
        has_modules=0
        break
      fi
    done

    if [ "$has_modules" -eq 1 ]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  return 1
}

run_python_backend_if_exists() {
  backend_dir="app/backend"

  if [ ! -f "$backend_dir/pyproject.toml" ]; then
    log "skip backend: pyproject.toml not found"
    return 0
  fi

  if ! python_bin="$(python_command_with_modules ruff mypy pytest)"; then
    log "skip backend: python with ruff, mypy, and pytest not found"
    return 0
  fi

  log "run backend ruff"
  (cd "$backend_dir" && "$python_bin" -m ruff check .)

  log "run backend mypy"
  (cd "$backend_dir" && "$python_bin" -m mypy app tests)

  log "run backend pytest"
  (cd "$backend_dir" && "$python_bin" -m pytest)
}

run_safety_evals_if_exists() {
  if [ ! -f "evals/scripts/run_safety_evals.py" ]; then
    log "skip safety evals: runner not found"
    return 0
  fi

  if ! python_bin="$(python_command_with_modules pytest)"; then
    log "skip safety evals: python with pytest not found"
    return 0
  fi

  log "run safety eval tests"
  "$python_bin" -m pytest evals/tests

  log "run safety eval cases"
  "$python_bin" evals/scripts/run_safety_evals.py

  log "run optional live Ollama eval gate"
  "$python_bin" -m evals.scripts.run_live_ollama_evals
}

run_rag_validation_if_exists() {
  if [ ! -f "rag/scripts/validate_sources.py" ]; then
    log "skip rag validation: source validator not found"
    return 0
  fi

  if ! python_bin="$(python_command_with_modules pytest)"; then
    log "skip rag validation: python with pytest not found"
    return 0
  fi

  log "run rag tests"
  "$python_bin" -m pytest rag/tests

  log "run rag source validation"
  "$python_bin" -m rag.scripts.validate_sources

  log "run rag ingestion"
  "$python_bin" -m rag.scripts.ingest_documents

  log "run rag hybrid index build"
  "$python_bin" -m rag.scripts.search_index --build
}

run_finetuning_validation_if_exists() {
  if [ "${GEMMA_SUS_VALIDATE_FINETUNING:-false}" != "true" ]; then
    log "skip fine-tuning validation: set GEMMA_SUS_VALIDATE_FINETUNING=true to run"
    return 0
  fi

  if [ ! -f "finetuning/scripts/validate_dataset.py" ]; then
    log "skip fine-tuning validation: dataset validator not found"
    return 0
  fi

  if ! python_bin="$(python_command_with_modules pytest)"; then
    log "skip fine-tuning validation: python with pytest not found"
    return 0
  fi

  log "run fine-tuning tests"
  "$python_bin" -m pytest finetuning/tests

  log "run fine-tuning dataset validation"
  "$python_bin" -m finetuning.scripts.validate_dataset
}

run_if_executable_exists() {
  file_path="$1"
  label="$2"

  if [ -x "$file_path" ]; then
    log "run $label"
    "$file_path"
  else
    log "skip $label: $file_path not executable or not found"
  fi
}

log "validate: start"

run_legacy_root_package_script_if_exists lint
run_legacy_root_package_script_if_exists typecheck
run_legacy_root_package_script_if_exists test
run_legacy_root_package_script_if_exists build
run_if_package_script_exists "app/frontend" lint
run_if_package_script_exists "app/frontend" typecheck
run_if_package_script_exists "app/frontend" test
run_if_package_script_exists "app/frontend" build
run_python_backend_if_exists
run_safety_evals_if_exists
run_rag_validation_if_exists
run_finetuning_validation_if_exists
run_if_executable_exists "./scripts/validate-extra.sh" "extra validation"

log "validate: complete"
