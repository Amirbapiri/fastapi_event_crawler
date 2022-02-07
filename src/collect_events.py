import json
import datetime
from typing import Iterator, Dict, Tuple

from celery import Celery
from celery.schedules import crontab

from scraper import Scraper


app = Celery("collect_events", broker="redis://localhost:6379/0")
app.conf.beat_schedule = {
    "crawl_and_get_events": {
        "task": "collect_events.start_crawling",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    }
}


class SaveEventsIntoJSON:
    def _date_range(
        self, start: datetime.date, end: datetime.date
    ) -> Iterator[datetime.date]:
        for day in range(int((end - start).days)):
            yield start + datetime.timedelta(day)

    def _get_current_date(self) -> Dict:
        current_year = datetime.datetime.today().strftime("%Y")
        current_month = datetime.datetime.today().strftime("%m")
        return {"year": int(current_year), "month": int(current_month)}

    def create_events_dictionary(self) -> Dict:
        events = dict()
        start_date = datetime.date(
            self._get_current_date()["year"], self._get_current_date()["month"], 1
        )
        end_date = datetime.date(
            self._get_current_date()["year"], self._get_current_date()["month"], 8
        )
        for date in self._date_range(start_date, end_date):
            month = date.strftime("%B").lower()
            if month not in events:
                events[month] = dict()
            events[month][date.day] = Scraper().events_of_the_day(
                month=month, day=date.day
            )
        return events

    def save(self):
        events = self.create_events_dictionary()
        with open("events.json", mode="w") as file:
            json.dump(events, file, ensure_ascii=False, indent=4)
        return "Saved!"

    def start(self):
        return self.save()


@app.task
def start_crawling():
    return SaveEventsIntoJSON().start()
