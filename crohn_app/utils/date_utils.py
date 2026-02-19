from datetime import date, datetime, timedelta


def today() -> date:
    return date.today()


def now() -> datetime:
    return datetime.now()


def days_ago(n: int) -> date:
    return date.today() - timedelta(days=n)
