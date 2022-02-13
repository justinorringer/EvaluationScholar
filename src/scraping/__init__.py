from typing import Optional
import urllib.parse

from scraping.parsing import parse_citations
from scraping.scraperapi import get_html

retry_count = 3

# TODO: Handle api errors
def scrape_citations(paper_title: str) -> Optional[int]:
    base_link = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C34&q=allintitle%3A+%22'
    base_link_end = '%22&btnG='

    encoded_title = urllib.parse.quote_plus(paper_title)

    url = base_link + encoded_title + base_link_end

    html = get_html(url)
    return parse_citations(html)