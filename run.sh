#!/bin/bash

ROOT_DIR=$(dirname "$(readlink -f "$0")")
CWD=$(pwd)

if [ -d "$1" ]; then
  cd "$1" || exit 1
else
  echo "Directory not provided or first argument is not a directory."
fi

TEMP_GITLOG=$(git log --pretty=format:'%H %cI')
export TEMP_GITLOG

validate_date() {
  local date_pattern='^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
  if [[ ! $1 =~ $date_pattern ]]; then
    echo "Invalid date format $1"
    exit 1
  fi
}

export START_DATE="$2"
export END_DATE="$3"
validate_date "$START_DATE"
validate_date "$END_DATE"

# shellcheck disable=SC2046
# shellcheck disable=SC2116
# shellcheck disable=SC2086
COMMIT_MAP=$(python "$ROOT_DIR"/commit_map.py $(echo $TEMP_GITLOG) --start-date "${START_DATE?}" --end-date "${END_DATE?}")
export COMMIT_MAP

git-filter-repo --force --commit-callback "commit_map = $COMMIT_MAP
$(cat "$ROOT_DIR"/commit-callback-body.py.txt)"

echo "Completed successfully."
git log
cd "$CWD" || exit 1
exit 0
