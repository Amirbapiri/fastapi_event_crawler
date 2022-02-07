from typing import List

import requests as _requests
import bs4 as _bs4


class Scraper:
    def _generate_url(self, month: str, day: int) -> str:
        url = f"https://www.onthisday.com/day/{month}/{day}"
        return url

    def _get_page(self, url: str) -> _bs4.BeautifulSoup:
        page = _requests.get(url)
        soup = _bs4.BeautifulSoup(page.content, "html.parser")
        return soup

    def events_of_the_day(self, month: str, day: int) -> List[str]:
        url = self._generate_url(month, day)
        page = self._get_page(url)
        raw_events = page.find_all(class_="event")
        events = [event.text for event in raw_events]
        return events
