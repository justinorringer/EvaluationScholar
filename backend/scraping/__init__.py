from typing import Optional, Tuple

from scraping.parsing import parse_citations, parse_papers, parse_year
from scraping.scraperapi import search_paper, get_html

def scrape_citations(paper_title: str) -> Optional[int]:
    html = search_paper(paper_title)
    papers = parse_papers(html)
    return parse_citations(papers[0])

def scrape_year(paper_title: str) -> Optional[int]:
    html = search_paper(paper_title)
    papers = parse_papers(html)
    return parse_year(papers[0])

def scrape_paper(paper_title: str) -> Tuple[Optional[int], Optional[int]]:
    html = search_paper(paper_title)
    papers = parse_papers(html)
    citations = parse_citations(papers[0])
    year = parse_year(papers[0])
    return citations, year