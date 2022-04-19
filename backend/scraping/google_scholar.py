from typing import Optional, List, Dict
from bs4 import BeautifulSoup
import re
import urllib.parse

from scraping.scraperapi import get_html

def search_papers(paper_title: str) -> List[Dict]:
    html = get_paper_search_html(paper_title)
    paper_blocks = parse_paper_blocks(html)
    papers = [parse_paper(paper_block) for paper_block in paper_blocks]

    return [paper for paper in papers if 'citation_entry' not in paper]

def search_profiles(author_name: str) -> List[Dict]:
    html = get_profile_search_html(author_name)
    profile_blocks = parse_profile_blocks(html)
    profiles = [parse_profile(profile_block) for profile_block in profile_blocks]

    return profiles

def get_paper_search_html(paper_title: str) -> str:
    base_link = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C34&q=allintitle%3A+%22'
    base_link_end = '%22&btnG='

    encoded_title = urllib.parse.quote_plus(paper_title)

    url = base_link + encoded_title + base_link_end

    return get_html(url)

def get_profile_search_html(author_name: str) -> str:
    base_link = "https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors="
    base_link_end = "&btnG="

    encoded_name = urllib.parse.quote_plus(author_name)

    url = base_link + encoded_name + base_link_end

    return get_html(url)

def get_profile_page_html(profile_id: str) -> str:
    base_link = "https://scholar.google.com/citations?user="
    base_link_end = "&hl=en&oi=sra"

    url = base_link + profile_id + base_link_end

    return get_html(url)

def parse_paper_blocks(scholar_search_html: str) -> List[str]:
    soup = BeautifulSoup(scholar_search_html, 'html.parser')

    return soup.find_all("div", {"class": "gs_ri"})

def is_citation_entry(paper: str) -> bool:
    h3 = paper.find("h3", {"class": "gs_rt"})

    if h3 is None:
        return False
    
    span = h3.find("span", {"class": "gs_ctu"})
    return span is not None

def parse_title(paper: str) -> Optional[str]:
    h3 = paper.find("h3", {"class": "gs_rt"})

    if h3 is None:
        return None

    title_container = h3.find("a")

    if title_container is None:
        title_container = h3.find("span", {"id": True})

        if title_container is None:
            return None
    
    # Remove any tags that may be in the title
    return re.sub(r'<[^>]*?>', '', title_container.text)

def parse_citations(paper: str) -> Optional[int]:
    link = paper.find("a", href=lambda href: href and href.startswith("/scholar?cites"))

    if link is None:
        return 0

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

def parse_paper_authors(paper: str) -> Optional[Dict]:
    div = paper.find("div", {"class": "gs_a"})

    if div is None:
        return None
    
    links = div.find_all("a")

    # TODO: Account for authors without a link

    return [{
        'name': re.sub(r'<[^>]*?>', '', link.text),
        'id': re.search("user=(.+)&hl=", link['href']).group(1)
    } for link in links]

def parse_paper(paper_block: str) -> Dict:
    citation_entry = is_citation_entry(paper_block)

    paper = {
        'title': parse_title(paper_block),
        'year': parse_year(paper_block),
        'id': parse_paper_id(paper_block),
        'citations': parse_citations(paper_block),
        'authors': parse_paper_authors(paper_block)
    }

    if citation_entry:
        paper['citation_entry'] = True
    
    return paper

def parse_profile_blocks(scholar_search_html: str) -> List[str]:
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
    
    m = re.search("user=(.+)", a['href'])
    return m.group(1)

def parse_profile(profile_block) -> Dict:
    return {
        'name': parse_profile_name(profile_block),
        'institution': parse_profile_institution(profile_block),
        'id': parse_profile_id(profile_block)
    }

def parse_profile_page_name(profile_page_html: str) -> Optional[str]:
    soup = BeautifulSoup(profile_page_html, 'html.parser')

    div = soup.find("div", {"id": "gsc_prf_in"})

    if div is None:
        return None

    return div.text