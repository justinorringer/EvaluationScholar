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

def parse_paper_id(paper: str) -> Optional[str]:
    h3 = paper.find("h3")

    if h3 is None:
        return None

    a = h3.find("a")

    if a is None:
        return None
    
    if not a.has_attr('id'):
        return None
    
    return a['id']
