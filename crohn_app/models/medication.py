from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional


@dataclass
class Medication:
    id: int
    name: str
    type: str
    frequency: str
    scheduled_time: time


@dataclass
class MedicationLog:
    id: int
    medication_id: int
    scheduled_datetime: datetime
    taken: int
    taken_time: Optional[datetime]
