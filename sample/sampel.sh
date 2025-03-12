for var in DBT_RUN DBT_TEST DBT_FRESHNESS DBT_SNAPSHOT DBT_RETRY; do
  value="${!var:-}"
  if [ -n "$value" ]; then
    echo "command: $value"
    if ! $value; then
      echo "Error: command '$value' failed" >&2
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
