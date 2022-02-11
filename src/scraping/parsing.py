from typing import Optional

from bs4 import BeautifulSoup

def parse_citations(scholar_search_html: str) -> Optional[int]:
    soup = BeautifulSoup(scholar_search_html, 'html.parser')

    links = soup.find_all('a')

    # Just find the first citation link and get the count
    for link in links:
        if '/scholar?cites' in link['href']:
            return int(link.text.replace('Cited by ', ''))

    return None