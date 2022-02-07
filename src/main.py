from fastapi import FastAPI

import services as _services


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to this bloody API"}


@app.get("/events")
async def get_all_events():
    events = _services.get_all_events()
    return events


@app.get("/events/today")
async def events_of_today():
    events = _services.get_today()
    return events


@app.get("/events/{month}")
async def get_events(month: str):
    events = _services.month_events(month)
    return events


@app.get("/events/{month}/{day}")
async def get_events(month: str, day: int):
    events = _services.month_day_event(month, day)
    return events
