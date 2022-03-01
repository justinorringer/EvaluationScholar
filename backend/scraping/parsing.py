from typing import Optional, List
from bs4 import BeautifulSoup
import re

def parse_papers(scholar_search_html: str) -> List[str]:
    soup = BeautifulSoup(scholar_search_html, 'html.parser')

    return soup.find_all("div", {"class": "gs_ri"})

def parse_citations(paper: str) -> Optional[int]:
    link = paper.find("a", href=lambda href: href and href.startswith("/scholar?cites"))

    if link is None:
        return None

    return int(link.text.replace('Cited by ', ''))

def parse_year(paper: str) -> Optional[int]:
    year_div = paper.find("div", {"class": "gs_a"})

    if year_div is None:
        return None

    year_match = re.search(r'(\d+) - .+$', year_div.text)

    if year_match is None:
        return None

    return int(year_match.group(1))