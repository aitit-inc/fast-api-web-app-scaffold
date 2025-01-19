"""Time services"""
from datetime import datetime, timezone


def to_utc(dt: datetime) -> datetime:
    """Convert a datetime to UTC"""
    if dt.tzinfo is None:
        # If there is no timezone info (naive datetime), treat it as UTC
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        # If there is a timezone, convert it to UTC
        dt = dt.astimezone(timezone.utc)
    return dt
