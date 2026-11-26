from datetime import date, datetime, timedelta

ROLLOVER_HOUR = 4
STREAK_MIN_MINUTES = 10

def study_day(now: datetime, rollover_hour: int = ROLLOVER_HOUR) -> date:
   return (now - timedelta(hours=rollover_hour)).date()

def minutes_per_day(sessions: list[dict]) -> dict[date, int]:
    totals: dict[date, int] = {}
    for session in sessions:
        day = date.fromisoformat(session["date"])
        totals[day] = totals.get(day, 0) + session["minutes"]
    return totals

def streak_days(sessions: list[dict], min_minutes: int = STREAK_MIN_MINUTES) -> set[date]:
    return {day for day, minutes in minutes_per_day(sessions).items() if minutes >= min_minutes}

def current_streak(
    sessions: list[dict],
    today: date,
    min_minutes: int = STREAK_MIN_MINUTES,
) -> int:
    days = streak_days(sessions, min_minutes)
    day = today if today in days else today - timedelta(days=1)
    streak = 0
    while day in days:
        streak += 1
        day -= timedelta(days=1)
    return streak

def best_streak(sessions: list[dict], min_minutes: int = STREAK_MIN_MINUTES) -> int:
    best = run = 0
    previous = None
    for day in sorted(streak_days(sessions, min_minutes)):
        if previous is not None and day - previous == timedelta(days=1):
            run += 1
        else:
            run = 1
        best = max(best, run)
        previous = day
    return best