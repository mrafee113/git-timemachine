#!/bin/bash

display_usage() {
  echo "Usage: $0 WD -st START_DATE -ed END_DATE [-m MIN_COMMITS] [-t TIMEZONE]"
  echo "Arguments:"
  echo "  WD                     : Positional argument, required"
  echo "  -st, --start-date      : Start date, required"
  echo "  -ed, --end-date        : End date, required"
  echo "  -m,  --minimum-commits : Minimum commits, optional (default: 0)"
  echo "  -t,  --timezone        : Timezone, optional"
}

# parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
  -sd | --start-date)
    START_DATE=$2
    shift 2
    ;;
  -ed | --end-date)
    END_DATE=$2
    shift 2
    ;;
  -m | --minimum-commits)
    MIN_COMMITS=$2
    shift 2
    ;;
  -t | --timezone)
    TIMEZONE=$2
    shift 2
    ;;
  *)
    WD=$1
    shift
    ;;
  esac
done

if [[ -z $WD || -z $START_DATE || -z $END_DATE ]]; then
  display_usage
  exit 1
fi

ROOT_DIR=$(dirname "$(readlink -f "$0")")

if [ ! -d "$WD/.git" ]; then
  git -C "$WD" init
  git branch -M main
fi

find_git_files() {
  local all_files
  all_files=$(find "$WD" -type f -not -path '*/\.git/*')
  all_files_array=()
  while IFS= read -r line; do
    all_files_array+=("$line")
  done <<< "$all_files"

  local ignored=()
  while read -r file; do
    if git -C "$WD" check-ignore -q "$file"; then
      ignored+=("$file")
    fi
  done <<< "$all_files"

  local unchanged=()
  while read -r file; do
    if [ -z "$(git -C "$WD" status --porcelain "$file")" ]; then
      unchanged+=("$file")
    fi
  done <<< "$all_files"

  # remove files from all_files_array
  for file in "${ignored[@]}"; do
    all_files_array=("${all_files_array[@]/$file}")
  done
  for file in "${unchanged[@]}"; do
    all_files_array=("${all_files_array[@]/$file}")
  done

  # remove empty elements and duplicates
  # shellcheck disable=SC2207
  all_files_array=($(echo "${all_files_array[@]}" | tr ' ' '\n' | sort -u))
  result=$(printf "%s\n" "${all_files_array[@]}")
  echo "$result"
}

# uncomment this if you wanted to change "git -C "$WD" add ." to something else.
# git -C "$WD" add .
# or this line
# local files=$(find "$WD" -type f -not -path '*/\.git/*' -not -path '.gitignore' |
#   while read -r file; do git check-ignore -q "$file" || echo "$file"; done)
# or this line
# files=$(git -C "$WD" ls-files)

files=$(find_git_files)
file_count=$(echo "$files" | wc -l)
file_count=$((file_count + 5))  # THIS IS BECAUSE BASH IS UNPREDICTABLE. MF'ER RANDOMLY LOST ME TWO DATETIMES.

OUTPUT=$(python3 "$ROOT_DIR/dates.py" -n "$file_count" -sd "$START_DATE" -ed "$END_DATE" -m "$MIN_COMMITS" -t "$TIMEZONE")
DATETIMES=()
while read -r -d ' ' element; do
  DATETIMES+=("$element")
done <<< "$OUTPUT"

counter=1
while IFS= read -r file; do
  # check if already added
  if [[ ! $(git -C "$WD" status --porcelain "$file" ) == A* ]]; then
    git -C "$WD" add "$file"
  fi

  DATE="${DATETIMES[$counter]}"
  if [ -z "$DATE" ]; then
    echo "empty date.. counter: $counter"
  fi
  DATE=$(date -d "$DATE" +"%Y-%m-%d %H:%M:%S %z")

  file=$(basename "$file")
  GIT_AUTHOR_DATE="$DATE" GIT_COMMITTER_DATE="$DATE" git commit -m "Added $file"

  counter=$((counter + 1))
done <<< "$files"

git log
exit 0
