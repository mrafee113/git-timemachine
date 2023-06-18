### Requirements

* git-filter-repo
    * Ubuntu 22.10: `sudo apt install git-filter-repo`

### Description
This project, is intended to fake git commit timestamps, therefore faking one's GitHub commit status.  
* Example usage:
```bash
chmod +x run.sh
# start and end date format: YYYY-MM-DD
START_DATE='2002-12-01'
END_DATE='2021-11-03'
path/to/run.sh path/to/git-repo "$START_DATE" "$END_DATE"
```
