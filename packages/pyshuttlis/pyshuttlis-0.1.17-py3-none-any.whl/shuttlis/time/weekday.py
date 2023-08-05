import calendar
from datetime import datetime, date
from enum import Enum
from functools import total_ordering


@total_ordering
class WeekDay(Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

    @classmethod
    def extract_from_datetime(cls, dt: datetime):
        return cls[calendar.day_name[dt.weekday()].upper()]

    @classmethod
    def extract_from_date(cls, dt: date):
        return cls[calendar.day_name[dt.weekday()].upper()]

    @classmethod
    def from_string(cls, weekday: str):
        return cls[weekday.upper()]

    def __str__(self):
        return str(self.name)

    def __lt__(self, other):
        return _order.index(self) < _order.index(other)


_order = [
    WeekDay.MONDAY,
    WeekDay.TUESDAY,
    WeekDay.WEDNESDAY,
    WeekDay.THURSDAY,
    WeekDay.FRIDAY,
    WeekDay.SATURDAY,
    WeekDay.SUNDAY,
]
