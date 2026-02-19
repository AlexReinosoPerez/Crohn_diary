from typing import List

import database.db as db
from models.medication import Medication
from utils.date_utils import today, now


def get_medications_for_today() -> List[Medication]:
    today_weekday = today().isoweekday()  # 1=Monday ... 7=Sunday
    rows = db.fetchall("SELECT * FROM medication")
    medications = []
    for row in rows:
        med = Medication(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            frequency=row["frequency"],
            scheduled_time=row["scheduled_time"],
        )
        if med.frequency == "daily":
            medications.append(med)
        elif med.frequency in ("weekly", "every_n_weeks"):
            # Schedule on Mondays by default (no interval metadata in schema)
            if today_weekday == 1:
                medications.append(med)
    return medications


def mark_medication_taken(medication_id: int) -> None:
    today_str = today().isoformat()
    existing = db.fetchone(
        """SELECT id FROM medication_log
           WHERE medication_id = ?
           AND DATE(scheduled_datetime) = ?""",
        (medication_id, today_str),
    )
    if existing:
        db.execute(
            """UPDATE medication_log SET taken = 1, taken_time = ?
               WHERE id = ?""",
            (now().isoformat(), existing["id"]),
        )
    else:
        db.execute(
            """INSERT INTO medication_log (medication_id, scheduled_datetime, taken, taken_time)
               VALUES (?, ?, 1, ?)""",
            (medication_id, now().isoformat(), now().isoformat()),
        )


def is_medication_taken_today(medication_id: int) -> bool:
    today_str = today().isoformat()
    row = db.fetchone(
        """SELECT taken FROM medication_log
           WHERE medication_id = ?
           AND DATE(scheduled_datetime) = ?
           AND taken = 1""",
        (medication_id, today_str),
    )
    return row is not None
