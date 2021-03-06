import functools
from datetime import datetime, time, date, timedelta

from flask import g, session, redirect

from estusshots import app

TIME_FMT = "%H:%M"
DATE_FMT = "%Y-%m-%d"


def str_to_datetime(data: str) -> datetime:
    """
    Convert %H:%M formatted string into a python datetime object
    """
    data = ":".join(data.split(":")[:2])
    return datetime.strptime(data, TIME_FMT)


def datetime_time_str(data: datetime) -> str:
    """
    Convert a datetime object into a formatted string for display
    :param data: datetime
    :return: str
    """
    return data.strftime(TIME_FMT)


def timedelta_to_str(data: timedelta) -> str:
    """
    Remove second and microsecond portion from timedeltas for display
    :param data: datetime.timedelta
    :return: str
    """
    return str(
        data - timedelta(seconds=data.seconds, microseconds=data.microseconds)
    )


def by_time(e):
    """
    Custom sort key for sorting by time codes in the format HH:MM
    This version sorts codes with hour '00' after '23'
    """
    if not hasattr(e, "time") or isinstance(e.time, time):
        return id(e)

    if e.time.hour == 0:
        return f"24{e.time.minute}"
    return f"{e.time.hour}{e.time.minute}"


def compute_timedelta(start: time, end: time) -> float:
    if not start or not end:
        return 0
    s = datetime.combine(date.today(), start)
    # Check if the the end is still on the same day
    if start.hour > end.hour:
        base = date.today() + timedelta(days=1)
    else:
        base = date.today()
    e = datetime.combine(base, end)
    difference = s - e
    difference_hours = difference.total_seconds() / 3600
    return abs(difference_hours)


def combine_datetime(date: datetime.date, time: datetime.time):
    """
    Combine a date and time object into a datetime object
    """
    return datetime(
        date.year,
        date.month,
        date.day,
        time.hour,
        time.minute,
        time.second,
        time.microsecond,
    )


def get_user_type(password):
    # TODO password hashing?
    if password == app.config.get("WRITE_PW"):
        return "editor"
    if password == app.config.get("READ_PW"):
        return "readonly"
    return False


def set_user_role(data):
    """Set the users role in the flask g object for later usage"""
    g.is_editor = data == "editor"


def authorize(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            set_user_role(session["user_type"])
        except KeyError:
            return redirect("/login")
        return func(*args, **kwargs)

    return wrapper


@app.template_filter("format_time")
def format_time(value):
    """Make the datetime to time string formatting available to jinja2"""
    if value is None:
        return ""
    return datetime_time_str(value)


@app.template_filter("format_timedelta")
def format_timedelta(value):
    """Make formatting for timedeltas available to jinja2"""
    if value is None:
        return ""
    return timedelta_to_str(value)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
