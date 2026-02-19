CREATE TABLE IF NOT EXISTS bowel_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('normal', 'diarrhea', 'urgency')),
    pain INTEGER -- boolean: 0 or 1, nullable
);

CREATE TABLE IF NOT EXISTS fatigue_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL UNIQUE,
    level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS medication (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('oral', 'injection', 'iv')),
    frequency TEXT NOT NULL CHECK(frequency IN ('daily', 'weekly', 'every_n_weeks')),
    scheduled_time TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS medication_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medication_id INTEGER NOT NULL REFERENCES medication(id),
    scheduled_datetime DATETIME NOT NULL,
    taken INTEGER NOT NULL DEFAULT 0,
    taken_time DATETIME
);

CREATE TABLE IF NOT EXISTS daily_activity (
    date DATE PRIMARY KEY,
    has_any_log INTEGER NOT NULL DEFAULT 0
);
