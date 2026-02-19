from dataclasses import dataclass
from datetime import date


@dataclass
class DailyActivity:
    date: date
    has_any_log: int
