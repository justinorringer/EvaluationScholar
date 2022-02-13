import requests
import os
from scraping.errors import ApiNoCreditsError, ApiRequestsFailedError

retry_count = 3

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
