import backend.scraping as scraping
import backend.scraping.parsing as parsing

def test_scraping():
    html = scraping.search_paper("Autonomous Aerial Water Sampling")
    papers = parsing.parse_papers(html)
    assert len(papers) > 0
    paper = papers[0]

    citations = parsing.parse_citations(paper)
    assert citations is not None
    assert citations > 0

    year = parsing.parse_year(paper)
    assert year is not None
    assert year == 2015

    id = parsing.parse_paper_id(paper)
    assert id is not None
    assert id == "bhfHsCHhomoJ"