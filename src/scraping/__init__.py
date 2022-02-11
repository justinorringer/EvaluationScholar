import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from typing import Optional

# TODO: Handle api errors
def scrape_citations(paper_title: str) -> Optional[int]:
    base_link = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C34&q=allintitle%3A+%22'
    base_link_end = '%22&btnG='

    encoded_title = urllib.parse.quote_plus(paper_title)

    url = base_link + encoded_title + base_link_end

    params = {'api_key': os.getenv('SCRAPER_API_KEY'), 'url': url}
    response = requests.get('https://api.scraperapi.com/', params=params)

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find('div', class_='gs_fl').find_all('a')

    for link in links:
        if '/scholar?cites' in link['href']:
            return int(link.text.replace('Cited by ', ''))

    return None