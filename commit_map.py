import json
import argparse

from random import randint
from datetime import datetime, date, timedelta, time as dtime


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('commits', nargs='+', help='List of commits')
    parser.add_argument('--start-date', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                        required=True, help="start-date (format: YYYY-MM-DD)")
    parser.add_argument('--end-date', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                        required=True, help="end-date (format: YYYY-MM-DD)")
    return parser.parse_args()


def parse_commits(commits: list[str]) -> list[tuple[str, datetime]]:
    hashes, dates = commits[0::2], commits[1::2]
    _new_commits = list()
    for chash, dt in zip(hashes, dates):
        dt = datetime.fromisoformat(dt)
        _new_commits.append((chash, dt))

    _new_commits.sort(key=lambda x: x[1])

    return _new_commits


def select_rand_time() -> dtime:
    # time boundary: 7:30 am - 11:00 pm
    return dtime(
        randint(7, 23),
        randint(0, 59),
        randint(0, 59)
    )


def renew_datetime(day: date, tz):
    return datetime.combine(
        day,
        select_rand_time(),
        tz
    )


def space_out(commits: list[tuple[str, datetime]], start_date: date, end_date: date):
    total_days = (end_date - start_date).days + 1
    total_commits = len(commits)
    commits_per_day = total_commits // total_days
    days_interval = total_days // total_commits
    extra_commits = total_commits % total_days

    current_date = start_date
    commit_index = 0

    for _ in range(total_days):
        daily_commits = commits_per_day
        if extra_commits > 0:
            daily_commits += 1
            extra_commits -= 1

        for _ in range(daily_commits):
            idx = min(commit_index, total_commits - 1) if \
                total_commits < total_days - 1 else commit_index
            chash, dt = commits[idx]
            dt = renew_datetime(current_date, dt.tzinfo)
            commits[idx] = (chash, dt)
            commit_index += 1

        interval = days_interval if total_commits < total_days - 1 else 1
        current_date += timedelta(days=interval)

    return commits


def export(commits: list[tuple[str, datetime]]):
    commit_map = {chash: dt for chash, dt in commits}
    for chash, dt in commit_map.items():
        dt = f"{int(dt.timestamp())} {dt.strftime('%z')}"
        commit_map[chash] = dt

    print(json.dumps(commit_map))


def main():
    args = parse_args()
    commits, start_date, end_date = args.commits, args.start_date, args.end_date
    commits = parse_commits(commits)
    commits = space_out(commits, start_date=start_date, end_date=end_date)
    export(commits)


if __name__ == '__main__':
    main()
