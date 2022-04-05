from typing import Optional, Tuple, Dict

from scraping.parsing import parse_paper, parse_paper_blocks, parse_profile, parse_profile_blocks
from scraping.scraperapi import search_paper, search_profile

def scrape_papers(paper_title: str) -> Dict:
    html = search_paper(paper_title)
    paper_blocks = parse_paper_blocks(html)

    return [parse_paper(paper_block) for paper_block in paper_blocks]

def scrape_profiles(profile_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    html = search_profile(profile_name)
    profile_blocks = parse_profile_blocks(html)

    return [parse_profile(profile) for profile in profile_blocks]