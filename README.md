# Crohn Clinical Log App

## Purpose

This is a local, single-user clinical tracking application for people with Crohn's disease.

The purpose of the app is strictly:

- To allow fast (<10 seconds) daily logging of structured clinical data.
- To generate clear summaries that can be shown during medical consultations.
- To avoid interpretation, prediction, or medical advice.

This is NOT:
- A diagnostic tool
- A medical advisor
- A treatment recommender
- A mental health or gamification platform

The system must remain simple, fast, and clinically neutral.

---

## Technical Stack

- Python 3.11+
- Streamlit (UI layer)
- SQLite (local persistence)
- No authentication
- No external services
- No backend API
- Single local user only

---

## Architectural Principles

1. Keep interactions minimal.
2. No text input for daily logs.
3. No confirmation dialogs.
4. Automatic saving.
5. Strict separation between UI and persistence.
6. No medical interpretations.
7. No gamification (mascot is cosmetic and optional).

---

## Functional Scope (MVP)

### Home Screen (Primary Screen)

This is the only daily-use screen.

It must contain:

1. Current date (read-only)
2. Medication block (if medication scheduled today)
   - "Mark as taken" button
   - Save timestamp automatically
3. Bowel logging
   - Buttons:
     - Normal
     - Diarrhea
     - Urgency
   - Optional pain toggle (Yes / No)
   - Automatic save with timestamp
4. Fatigue logging
   - Scale 1–5
   - Once per day
   - If already logged, show value instead of buttons
5. Secondary button:
   - "View consultation summary"

No additional features allowed.

---

## Consultation View

Secondary screen only.

Shows:
- Bowel movements per day (last 30/90 days)
- Days with diarrhea
- Medication adherence
- Average fatigue

No interpretation.
No alerts.
No predictions.

Export:
- CSV (PDF optional, not required for MVP)

---

## Data Model

SQLite database required.

Tables:

### bowel_log
- id (integer, primary key)
- timestamp (datetime)
- type (normal | diarrhea | urgency)
- pain (boolean or null)

### fatigue_log
- id (integer, primary key)
- date (date)
- level (integer 1–5)

### medication
- id (integer, primary key)
- name (text)
- type (oral | injection | iv)
- frequency (daily | weekly | every_n_weeks)
- scheduled_time (time)

### medication_log
- id (integer, primary key)
- medication_id (foreign key)
- scheduled_datetime (datetime)
- taken (boolean)
- taken_time (datetime)

### daily_activity
- date (primary key)
- has_any_log (boolean)

Important:
- daily_activity is factual only.
- It must not store streaks or gamification data.

---

## Project Structure (Expected)

```
crohn_app/
│
├── app.py
│
├── config/
│   └── settings.py
│
├── database/
│   ├── db.py
│   ├── schema.sql
│   └── migrations.py (optional, minimal)
│
├── models/
│   ├── bowel.py
│   ├── fatigue.py
│   ├── medication.py
│   └── activity.py
│
├── services/
│   ├── logging_service.py
│   ├── medication_service.py
│   └── summary_service.py
│
├── ui/
│   ├── home.py
│   └── consultation.py
│
└── utils/
    └── date_utils.py
```

Rules:
- UI must not contain SQL.
- Database logic must not contain Streamlit.
- Services coordinate between UI and models.
- No unnecessary abstraction layers.

---

## Mascot (Phase 2)

The mascot is optional and purely cosmetic.

Strict rules:
- It reads ONLY from `daily_activity`.
- It does NOT read bowel type.
- It does NOT read fatigue.
- It does NOT read medication.
- It does NOT interpret health.
- It does NOT generate messages.
- It does NOT create streaks.

If removed, the app must behave identically.

---

## Forbidden Features

Do NOT implement:

- Notifications
- Motivational messages
- Streak counters
- Rewards or punishments
- Free text notes
- AI
- Predictions
- Medical recommendations
- Multi-user support
- Cloud deployment

---

## Non-Goals

This project does NOT aim to:
- Replace medical care
- Provide disease monitoring analytics
- Act as a telemedicine platform
- Integrate with hospital systems

---

## Implementation Rules

- Keep code readable and minimal.
- Avoid premature optimization.
- Avoid complex patterns.
- Use simple SQLite queries.
- Ensure database initializes automatically if not present.
- Use large buttons in Streamlit.
- Auto-save interactions.

---

## Expected Deliverables

1. Working Home screen
2. Working SQLite initialization
3. Clean separation between UI and persistence
4. Consultation summary screen
5. CSV export functionality

Do not expand scope.
Follow the specification strictly.