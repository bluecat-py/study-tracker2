import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

#INCOMING
class SubjectIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=60)

class SessionIn(BaseModel):
    subject_id: int
    minutes: int = Field(gt=0, le=1440)
    date: dt.date | None = None
    note: str | None = Field(default=None, max_length=500)

#OUTGOING
class SubjectOut(BaseModel):
    id: int
    name: str
    archived: bool

class SessionOut(BaseModel):
    id: int
    subject: str
    minutes: int
    date: str
    source: str
    note: str | None

class Created(BaseModel):
    id: int

class TodayOut(BaseModel):
    date: str
    minutes_today: int
    daily_goal: int
    current_streak: int
    best_streak: int
