import argparse

from random import randint
from datetime import datetime, date, timedelta, time as dtime


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number-of-files', type=int, required=True,
                        help='integer indicating the number of files')
    parser.add_argument('-m', '--min-commits-per-day', required=False, default=0,
                        help='integer indicating minimum number of commits per day')
    parser.add_argument('-sd', '--start-date', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                        required=True, help="start-date (format: YYYY-MM-DD)")
    parser.add_argument('-ed', '--end-date', type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
                        required=True, help="end-date (format: YYYY-MM-DD)")
    args = parser.parse_args()
    n, sd, ed, m = args.number_of_files, args.start_date, args.end_date, args.min_commits_per_day

    if m is None or not m:
        m = 0
    else:
        try:
            m = int(m)
        except (TypeError, ValueError):
            m = 0

    return n, sd, ed, m


def select_rand_time() -> dtime:
    # time boundary: 7:30 am - 11:00 pm
    return dtime(
        randint(7, 23),
        randint(0, 59),
        randint(0, 59)
    )


def renew_datetime(day: date):
    return datetime.combine(
        day,
        select_rand_time(),
        datetime.now().astimezone().tzinfo
    )


def space_out(number_of_files: int, start_date: date, end_date: date, min_commits_per_day: int = 0) -> list[date]:
    total_days = (end_date - start_date).days + 1
    commits_per_day = number_of_files // total_days
    days_interval = total_days // number_of_files
    if min_commits_per_day:
        days_interval *= min_commits_per_day
    extra_commits = number_of_files % total_days

    current_date = start_date

    dates: list[date] = list()
    for _ in range(total_days):
        daily_commits = commits_per_day
        if extra_commits > 0:
            daily_commits += 1
            extra_commits -= 1

        if min_commits_per_day and min_commits_per_day > daily_commits:
            daily_commits = min_commits_per_day

        for _ in range(daily_commits):
            if len(dates) >= number_of_files:
                return dates

            dates.append(current_date)

        if number_of_files < total_days - 1:
            interval = days_interval
        else:
            interval = 1
            if min_commits_per_day:
                interval = min_commits_per_day // (number_of_files // total_days)
        current_date += timedelta(days=interval)

    return dates


def export(dates: list[datetime]):
    print(" ".join([
        dt.isoformat() for dt in dates
    ]))


def main():
    number_of_files, start_date, end_date, min_commits_per_day = parse_args()

    dates = space_out(number_of_files, start_date, end_date, min_commits_per_day)
    dates = [renew_datetime(dt) for dt in dates]
    dates.sort()
    export(dates)


if __name__ == '__main__':
    main()
