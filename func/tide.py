import datetime as dt


def get_dates(date_target: str) -> tuple[dt.datetime, dt.datetime]:
    dt_format = '%Y-%m-%d'
    dt_start = dt.datetime.strptime(date_target, dt_format)
    day1 = dt.timedelta(days=1)
    dt_end = dt_start + day1

    return dt_start, dt_end
