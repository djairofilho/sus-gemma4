#!/usr/bin/env sh
set -eu

log() {
  printf '%s\n' "$1"
}

run_if_package_script_exists() {
  script_name="$1"

  if [ ! -f package.json ]; then
    log "skip $script_name: package.json not found"
    return 0
  fi

  if command -v node >/dev/null 2>&1; then
    if node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts['$script_name'] ? 0 : 1)"; then
      if [ -f pnpm-lock.yaml ] && command -v pnpm >/dev/null 2>&1; then
        log "run pnpm $script_name"
        pnpm "$script_name"
      elif [ -f yarn.lock ] && command -v yarn >/dev/null 2>&1; then
        log "run yarn $script_name"
        yarn "$script_name"
      elif [ -f package-lock.json ] && command -v npm >/dev/null 2>&1; then
        log "run npm run $script_name"
        npm run "$script_name"
      elif command -v npm >/dev/null 2>&1; then
        log "run npm run $script_name"
        npm run "$script_name"
      else
        log "skip $script_name: no supported package manager found"
      fi
    else
      log "skip $script_name: package script not defined"
    fi
  else
    log "skip $script_name: node not found"
  fi
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

run_if_package_script_exists lint
run_if_package_script_exists typecheck
run_if_package_script_exists test
run_if_package_script_exists build
run_if_executable_exists "./scripts/validate-extra.sh" "extra validation"

log "validate: complete"
