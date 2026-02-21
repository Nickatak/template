#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/validate-env.sh <mode> <env-file>

Modes:
  local
  docker
  prod
EOF
}

if [[ $# -ne 2 ]]; then
  usage
  exit 2
fi

mode="$1"
env_file="$2"

if [[ ! -f "$env_file" ]]; then
  echo "Missing env file: $env_file"
  exit 1
fi

require_vars() {
  local missing=0
  for name in "$@"; do
    if [[ -z "${!name:-}" ]]; then
      echo "Missing required variable: $name"
      missing=1
    fi
  done

  if [[ "$missing" -ne 0 ]]; then
    exit 1
  fi
}

set -a
# shellcheck source=/dev/null
. "$env_file"
set +a

case "$mode" in
  local)
    require_vars SECRET_KEY JWT_SECRET DATABASE_URL NEXT_PUBLIC_API_URL
    ;;
  docker)
    require_vars SECRET_KEY MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD MYSQL_ROOT_PASSWORD
    ;;
  prod)
    require_vars SECRET_KEY JWT_SECRET STAGING_DATABASE_URL STAGING_ALLOWED_HOSTS STAGING_CORS_ALLOWED_ORIGINS STAGING_CSRF_TRUSTED_ORIGINS STAGING_NEXT_PUBLIC_API_URL STAGING_MYSQL_DATABASE STAGING_MYSQL_USER STAGING_MYSQL_PASSWORD STAGING_MYSQL_ROOT_PASSWORD
    ;;
  *)
    echo "Unknown mode: $mode"
    usage
    exit 2
    ;;
esac

echo "Environment validation passed for mode '$mode' using '$env_file'."
