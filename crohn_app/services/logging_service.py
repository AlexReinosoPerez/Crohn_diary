from typing import Optional

import database.db as db
from utils.date_utils import today, now


def log_bowel(bowel_type: str, pain: Optional[bool]) -> None:
    pain_val = int(pain) if pain is not None else None
    db.execute(
        "INSERT INTO bowel_log (timestamp, type, pain) VALUES (?, ?, ?)",
        (now().isoformat(), bowel_type, pain_val),
    )
    _update_daily_activity()


def log_fatigue(level: int) -> None:
    today_str = today().isoformat()
    existing = db.fetchone(
        "SELECT id FROM fatigue_log WHERE date = ?", (today_str,)
    )
    if existing is None:
        db.execute(
            "INSERT INTO fatigue_log (date, level) VALUES (?, ?)",
            (today_str, level),
        )
        _update_daily_activity()


def get_today_fatigue() -> Optional[int]:
    row = db.fetchone(
        "SELECT level FROM fatigue_log WHERE date = ?", (today().isoformat(),)
    )
    return row["level"] if row else None


def _update_daily_activity() -> None:
    today_str = today().isoformat()
    db.execute(
        """INSERT INTO daily_activity (date, has_any_log)
           VALUES (?, 1)
           ON CONFLICT(date) DO UPDATE SET has_any_log = 1""",
        (today_str,),
    )
