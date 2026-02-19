import csv
import io
from typing import Dict

import database.db as db
from utils.date_utils import days_ago, today


def get_bowel_summary(days: int) -> Dict:
    start = days_ago(days).isoformat()
    rows = db.fetchall(
        """SELECT DATE(timestamp) as day, type, COUNT(*) as count
           FROM bowel_log
           WHERE DATE(timestamp) >= ?
           GROUP BY day, type""",
        (start,),
    )
    total_per_day: Dict[str, int] = {}
    diarrhea_days = set()
    for row in rows:
        day = row["day"]
        total_per_day[day] = total_per_day.get(day, 0) + row["count"]
        if row["type"] == "diarrhea":
            diarrhea_days.add(day)

    movements_per_day = (
        sum(total_per_day.values()) / len(total_per_day) if total_per_day else 0.0
    )
    return {
        "movements_per_day": round(movements_per_day, 2),
        "days_with_diarrhea": len(diarrhea_days),
    }


def get_fatigue_summary(days: int) -> Dict:
    start = days_ago(days).isoformat()
    row = db.fetchone(
        """SELECT AVG(level) as avg_level
           FROM fatigue_log
           WHERE date >= ?""",
        (start,),
    )
    avg = row["avg_level"] if row and row["avg_level"] is not None else None
    return {"average_fatigue": round(avg, 2) if avg is not None else None}


def get_medication_adherence(days: int) -> Dict:
    start = days_ago(days).isoformat()
    total_row = db.fetchone(
        """SELECT COUNT(*) as total FROM medication_log
           WHERE DATE(scheduled_datetime) >= ?""",
        (start,),
    )
    taken_row = db.fetchone(
        """SELECT COUNT(*) as taken FROM medication_log
           WHERE DATE(scheduled_datetime) >= ?
           AND taken = 1""",
        (start,),
    )
    total = total_row["total"] if total_row else 0
    taken = taken_row["taken"] if taken_row else 0
    adherence = (taken / total * 100) if total > 0 else None
    return {"adherence_percentage": round(adherence, 1) if adherence is not None else None}


def export_csv(days: int) -> str:
    bowel = get_bowel_summary(days)
    fatigue = get_fatigue_summary(days)
    medication = get_medication_adherence(days)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["metric", "value"])
    writer.writerow(["period_days", days])
    writer.writerow(["bowel_movements_per_day", bowel["movements_per_day"]])
    writer.writerow(["days_with_diarrhea", bowel["days_with_diarrhea"]])
    writer.writerow(["average_fatigue", fatigue["average_fatigue"]])
    writer.writerow(["medication_adherence_pct", medication["adherence_percentage"]])
    return output.getvalue()
