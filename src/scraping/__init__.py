import requests
import os
from typing import Optional
import urllib.parse

from bs4 import BeautifulSoup

retry_count = 3

class ApiError(Exception):
    pass

class ApiNoCreditsError(ApiError):
    pass

class ApiRequestsFailedError(ApiError):
    pass

# TODO: Handle api errors
def scrape_citations(paper_title: str) -> Optional[int]:
    base_link = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C34&q=allintitle%3A+%22'
    base_link_end = '%22&btnG='

    encoded_title = urllib.parse.quote_plus(paper_title)

    url = base_link + encoded_title + base_link_end

    params = {'api_key': os.getenv('SCRAPER_API_KEY'), 'url': url}

    for _ in range(retry_count):
        response = requests.get('https://api.scraperapi.com/', params=params)

        # Sometimes, ScraperAPI returns a 500 error. They ask that you retry at least three times.
        if(response.status_code == 500):
            continue

        if(response.status_code == 403):
            raise ApiNoCreditsError

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a')

        # Just find the first citation link and get the count
        for link in links:
            if '/scholar?cites' in link['href']:
                return int(link.text.replace('Cited by ', ''))

        return None

    raise ApiRequestsFailedError