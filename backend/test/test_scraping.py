import backend.scraping as scraping
import backend.scraping.scraperapi as scraperapi
import backend.scraping.parsing as parsing
import pytest

@pytest.mark.scraping
def test_papers():
    html = scraperapi.search_paper("Autonomous Aerial Water Sampling")
    papers = parsing.parse_papers(html)
    assert len(papers) > 0
    paper = papers[0]

    citations = parsing.parse_citations(paper)
    assert citations > 0

    year = parsing.parse_year(paper)
    assert year == 2015

    id = parsing.parse_paper_id(paper)
    assert id == "bhfHsCHhomoJ"

@pytest.mark.scraping
def test_profiles():
    html = scraperapi.search_profile("douglas G altman")
    profiles = parsing.parse_profiles(html)
    assert len(profiles) > 0
    profile = profiles[0]

    name = parsing.parse_profile_name(profile)
    assert name == "Douglas G Altman"

    institution = parsing.parse_profile_institution(profile)
    assert institution == "Centre for Statistics in Medicine, University of Oxford"

    id = parsing.parse_profile_id(profile)
    assert id == "QnLm3kAAAAJ"