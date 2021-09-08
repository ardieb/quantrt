from datetime import datetime, timedelta

from quantrt.common.timescale import Timescale


__all__ = ["datetime_floor"]


def datetime_floor(dt: datetime, scale: Timescale) -> datetime:
    if scale == Timescale.Minute:
        return dt.replace(second = 0, microsecond = 0)
    if scale == Timescale.FiveMinute:
        return dt.replace(minute = (dt.minute // 5) * 5, second = 0, microsecond = 0)
    if scale == Timescale.FifteenMinute:
        return dt.replace(minute = (dt.minute // 15) * 15, second = 0, microsecond = 0)
    if scale == Timescale.ThirtyMinute:
        return dt.replace(minute = (dt.minute // 30) * 30, second = 0, microsecond = 0)
    if scale == Timescale.Hour:
        return dt.replace(minute = 0, second = 0, microsecond = 0)
    if scale == Timescale.SixHour:
        return dt.replace(hour = (dt.hour // 6) * 6, minute = 0, second = 0, microsecond = 0)
    if scale == Timescale.Day:
        return dt.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    # Fall through for unknown
    return dt