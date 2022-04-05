from typing import Optional, Tuple, Dict

import scraping.google_scholar as google_scholar

def scrape_papers(paper_title: str) -> Dict:
    return google_scholar.search_papers(paper_title)

def scrape_profiles(profile_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    return google_scholar.search_profiles(profile_name)