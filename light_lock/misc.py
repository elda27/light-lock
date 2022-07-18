from datetime import timedelta


def to_timedelta_ext(time: str) -> timedelta:
    """Convert a string to a timedelta."""
    time = time.lower()
    if time.endswith("s"):
        return timedelta(seconds=float(time[:-1]))
    elif time.endswith("m"):
        return timedelta(minutes=float(time[:-1]))
    elif time.endswith("h"):
        return timedelta(hours=float(time[:-1]))
    elif time.endswith("d"):
        return timedelta(days=float(time[:-1]))
    elif time.endswith("w"):
        return timedelta(weeks=float(time[:-1]))
    else:
        try:
            return timedelta(seconds=float(time))
        except Exception:
            raise ValueError(f"Invalid time format: {time}")
