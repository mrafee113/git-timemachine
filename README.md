### Description
This project, is intended to warp (winks) git commit timestamps, therefore changing one's GitHub commit status.  
* Example usage:
```bash
chmod +x run.sh
# start and end date format: YYYY-MM-DD

# Usage: ./run.sh WD -st START_DATE -ed END_DATE [-m MIN_COMMITS] [-t TIMEZONE]
# Arguments:
#   WD                     : Positional argument, required
#   -st, --start-date      : Start date, required
#   -ed, --end-date        : End date, required
#   -m,  --minimum-commits : Minimum commits, optional (default: 0)

path/to/run.sh -sd '2020-01-01' -ed '2021-02-01' -m 2 path/to/project
path/to/run.sh -sd '2020-01-01' -ed '2021-02-01' path/to/project
```

### Disclaimer
I used this to create repos for my old uni projects and commit files. but somehow the files were overwritten with jargon; the original files were lost; don't use this till I figure it out.
