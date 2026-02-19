from dataclasses import dataclass
from datetime import date


@dataclass
class FatigueLog:
    id: int
    date: date
    level: int
