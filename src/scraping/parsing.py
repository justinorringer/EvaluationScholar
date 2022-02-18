from typing import Optional
from bs4 import BeautifulSoup
import re

def parse_papers(scholar_search_html: str) -> list[str]:
    soup = BeautifulSoup(scholar_search_html, 'html.parser')

    return soup.find_all("div", {"class": "gs_ri"})

def parse_citations(paper: str) -> Optional[int]:
    link = paper.find("a", href=lambda href: href and href.startswith("/scholar?cites"))

    if link is None:
        return None

    return link.text.replace('Cited by ', '')
    