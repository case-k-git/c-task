#!/bin/bash
# 注意: set -e を使うとエラー時に自動終了してしまうので使わない

for var in DBT_RUN DBT_TEST DBT_FRESHNESS DBT_SNAPSHOT DBT_RETRY; do
  value="${!var:-}"
  if [ -n "$value" ]; then
    echo "command: $value"
    if ! $value; then
      echo "Error: command '$value' failed" >&2
      # DBT_RUN, DBT_RETRY, DBT_SNAPSHOT の場合はスクリプトを終了しない
      case "$var" in
        DBT_RUN|DBT_RETRY|DBT_SNAPSHOT)
          echo "Skipping $var despite error"
          continue
          ;;
        *)
          exit 1
          ;;
      esac
    fi
  else
    echo "$var is not set"
  fi
done
