from datetime import datetime, timedelta
from enum import Enum


__all__ = ["Timescale"]


class Timescale(Enum):
    Minute = "1M"
    FiveMinute = "5M"
    FifteenMinute = "15M"
    ThirtyMinute = "30M"
    Hour = "1H"
    SixHour = "6H"
    Day = "1D"


    @property
    def unit(self) -> str:
        if self == Timescale.Minute: return "1M"
        elif self == Timescale.FiveMinute: return "5M"
        elif self == Timescale.FifteenMinute: return "1M"
        elif self == Timescale.ThirtyMinute: return "1M"
        elif self == Timescale.Hour: return "1H"
        elif self == Timescale.SixHour: return "1H"
        elif self == Timescale.Day: return "1D"
        raise ValueError("Unknow type for `Timescale`")
    

    @property
    def timedelta(self) -> timedelta:
        if self == Timescale.Minute: return timedelta(minutes = 1)
        elif self == Timescale.FiveMinute: return timedelta(minutes = 5)
        elif self == Timescale.FifteenMinute: return timedelta(minutes = 15)
        elif self == Timescale.ThirtyMinute: return timedelta(minutes = 30)
        elif self == Timescale.Hour: return timedelta(hours = 1)
        elif self == Timescale.SixHour: return timedelta(hours = 6)
        elif self == Timescale.Day: return timedelta(days = 1)
        raise ValueError("Unknow type for `Timescale`")
