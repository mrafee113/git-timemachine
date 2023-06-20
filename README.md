### Requirements

* git-filter-repo
    * Ubuntu 22.10: `sudo apt install git-filter-repo`

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
#   -t,  --timezone        : Timezone, optional

path/to/run.sh -sd '2020-01-01' -ed '2021-02-01' -m 2 -t "Asia/Tehran" path/to/project
path/to/run.sh -sd '2020-01-01' -ed '2021-02-01' path/to/project
```
