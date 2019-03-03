import datetime

TIME_FMT = "%H:%M"
DATE_FMT = "%Y-%m-%d"


def str_to_datetime(data: str) -> datetime.datetime:
    """
    Convert %H:%M formatted string into a python datetime object
    """
    data = ":".join(data.split(":")[:2])
    return datetime.datetime.strptime(data, TIME_FMT)


def datetime_time_str(data: datetime) -> str:
    """
    Convert a datetime object into a formatted string for display
    :param data: datetime
    :return: str
    """
    return data.strftime(TIME_FMT)


def timedelta_to_str(data: datetime.timedelta) -> str:
    """
    Remove second and microsecond portion from timedeltas for display
    :param data: datetime.timedelta
    :return: str
    """
    return str(
        data - datetime.timedelta(seconds=data.seconds, microseconds=data.microseconds)
    )


def combine_datetime(date: datetime.date, time: datetime.time):
    """
    Combine a date and time object into a datetime object
    """
    return datetime.datetime(
        date.year,
        date.month,
        date.day,
        time.hour,
        time.minute,
        time.second,
        time.microsecond,
    )
