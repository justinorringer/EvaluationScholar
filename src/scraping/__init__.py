from typing import Optional

from scraping.parsing import parse_citations, parse_papers
from scraping.scraperapi import search_paper, get_html

def scrape_citations(paper_title: str) -> Optional[int]:
    html = search_paper(paper_title)
    papers = parse_papers(html)
    return parse_citations(papers[0])