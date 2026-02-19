from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BowelLog:
    id: int
    timestamp: datetime
    type: str
    pain: Optional[int]
