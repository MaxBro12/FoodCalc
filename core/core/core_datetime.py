from datetime import timedelta, datetime, timezone
from time import time


def current_datetime() -> datetime:
    return datetime.now()


def time_delta(date_time: datetime) -> timedelta:
    return date_time - current_datetime()


def utc_time() -> datetime:
    return datetime.now(timezone.utc)


def unix_time() -> float:
    return time()