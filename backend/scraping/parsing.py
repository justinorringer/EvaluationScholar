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
    
    return a['id']

def parse_profiles(scholar_search_html: str) -> List[str]:
    soup = BeautifulSoup(scholar_search_html, 'html.parser')

    return soup.find_all("div", {"class": "gs_ai_chpr"})

def parse_profile_name(profile: str) -> Optional[str]:
    a = profile.find("a", {"class": "gs_ai_pho"})

    if a is None:
        return None

    span = a.find("span")

    if span is None:
        return None
    
    img = span.find("img")

    if img is None:
        return None

    return img['alt']

def parse_profile_institution(profile: str) -> Optional[str]:
    div = profile.find("div", {"class": "gs_ai_aff"})

    if div is None:
        return None
    
    return div.text

def parse_profile_id(profile: str) -> Optional[str]:
    a = profile.find("a", {"class": "gs_ai_pho"})

    if a is None:
        return None
    
    m = re.search("user=_(\w+)", a['href'])
    return m.group(1)