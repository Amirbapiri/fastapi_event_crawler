import json
import datetime
from typing import Dict


def get_all_events() -> Dict:
    with open("events.json") as file:
        data = json.load(file)
    return data


def month_events(month: str) -> Dict:
    """
    returns events for a particular month
    """
    events = get_all_events()
    valid_months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    try:
        if month.lower() in valid_months:
            month_events = events[month]
            return month_events
        return f"Given month: {month.lower()} is not valid."
    except KeyError:
        return "Couldn't find any event for the given month."


def month_day_event(month: str, day: int) -> Dict:
    """
    returns events for a particular month and day
    """
    events = get_all_events()
    valid_months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    try:
        if month.lower() in valid_months and day in range(1, 32):
            events = events[month]
            if str(day) in events:
                return events[str(day)]
            return f"Couldn't find any events for the given day."
        return f"Given date is not valid. Check it!"
    except KeyError:
        return "Couldn't find any event for the given date."


def get_today():
    today = datetime.date.today()
    month = today.strftime("%B")
    return month_day_event(month, today.day)
