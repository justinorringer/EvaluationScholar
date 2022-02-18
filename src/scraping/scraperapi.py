import requests
import os
from scraping.errors import ApiNoCreditsError, ApiRequestsFailedError
import urllib.parse

retry_count = 3

def search_paper(paper_title: str) -> str:
    base_link = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C34&q=allintitle%3A+%22'
    base_link_end = '%22&btnG='

    encoded_title = urllib.parse.quote_plus(paper_title)

    url = base_link + encoded_title + base_link_end

    html = get_html(url)
    return html

def get_html(url: str) -> str:
    params = {'api_key': os.getenv('SCRAPER_API_KEY'), 'url': url}

    for _ in range(retry_count):
        response = requests.get('https://api.scraperapi.com/', params=params)

        # Sometimes, ScraperAPI returns a 500 error. They ask that you retry at least three times.
        if(response.status_code == 500):
            continue

        if(response.status_code == 403):
            raise ApiNoCreditsError
        
        return response.text
    
    raise ApiRequestsFailedError
