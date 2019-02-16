import datetime

TIME_FMT = "%H:%M"
DATE_FMT = "%Y-%m-%d"


def str_to_time(data: str) -> datetime.time:
    data = ":".join(data.split(":")[:2])
    return datetime.datetime.strptime(data, TIME_FMT).time()


def time_to_str(data: datetime.time) -> str:
    """
    Convert a datetime.time object into a formatted string for sqlite
    :param data: datetime.time
    :return: str
    """
    return data.strftime(TIME_FMT)
