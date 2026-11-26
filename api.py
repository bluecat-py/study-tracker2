from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastApi, HTTPException, Query
import storage
from models import Created, SessionIn, SessionOut, SubjectIn, SubjectOut, TodayOut
from stats import best_streak, current_streak, minutes_per_day, study_day

DAILY_GOAL_MINUTES = 60 #Setting


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_db()
    yield


app = FastAPI(title="Study Tracker", lifespan=lifespan)

#SUBJECTS
@app.get("/api/subjects", response_model=list[SubjectOut])
def get_subject():
    return storage.list_subjects()

@app.post("/api/subjects", response_model=SubjectOut, status_code=201)
def create_subject(payload: SubjectIn):
    try:
        subject_id = storage.add_subject(payload.name)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from None
        return {"id": subject_id, "name": payload.name, "archived": False}

#SESSIONS
@app.get("/api/sessions", response_model=list[SessionOut])
def get_sessions(limit: int | None = Query(default=None, ge=1, le=500)):
    return storage.list_sessions(limit=limit)

@app.post("/api/sessions", response_model=Created, status_code=201)
def create_session(payload: SessionIn):
    if payload.date:
        day = payload.date.isoformat()
    else:
        day = None
    try:
        session_id = storage.add_session(payload.subject_id, payload.minutes, day=day, note=payload.note)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from None
    return {"id": session_id}

#TODAY
@app.get("/api/today", response_model=TodayOut)
def get_today():
    sessions = storage.list_sessions()
    today = study_day(datetime.now())
    return {
        "date": today.isoformat(),
        "minutes_today": minutes_per_day(sessions).get(today, 0),
        "daily_goal": DAILY_GOAL_MINUTES,
        "current_streak": current_streak(sessions, today),
        "best_streak": best_streak(sessions),
    }