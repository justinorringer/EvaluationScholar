import backend.scraping as scraping
import backend.scraping.scraperapi as scraperapi
import backend.scraping.parsing as parsing
import pytest

@pytest.mark.scraping
def test_profiles():
    #Test Google Scholar searching and parsing

    html = scraperapi.search_profile("douglas G altman")
    profile_blocks = parsing.parse_profile_blocks(html)
    assert len(profile_blocks) > 0
    
    profile_block = profile_blocks[0]
    profile = parsing.parse_profile(profile_block)

    name = parsing.parse_profile_name(profile_block)
    assert name == "Douglas G Altman"

    institution = parsing.parse_profile_institution(profile_block)
    assert institution == "Centre for Statistics in Medicine, University of Oxford"

    id = parsing.parse_profile_id(profile_block)
    assert id == "_QnLm3kAAAAJ"

    assert profile["name"] == "Douglas G Altman"
    assert profile["institution"] == "Centre for Statistics in Medicine, University of Oxford"
    assert profile["id"] == "_QnLm3kAAAAJ"

    # Test all-in-one call

    profiles = scraping.scrape_profiles("douglas G altman")
    assert len(profiles) > 0
    assert profiles[0]["name"] == "Douglas G Altman"
    assert profiles[0]["institution"] == "Centre for Statistics in Medicine, University of Oxford"
    assert profiles[0]["id"] == "_QnLm3kAAAAJ"

@pytest.mark.scraping
def test_papers():
    # Test Google Scholar searching and parsing

    html = scraperapi.search_paper("Autonomous Aerial Water Sampling")
    paper_blocks = parsing.parse_paper_blocks(html)
    assert len(paper_blocks) > 0

    paper_block = paper_blocks[0]
    paper = parsing.parse_paper(paper_block)

    citations = parsing.parse_citations(paper_block)
    assert citations > 0

    year = parsing.parse_year(paper_block)
    assert year == 2015

    id = parsing.parse_paper_id(paper_block)
    assert id == "bhfHsCHhomoJ"

    assert paper["citations"] > 0
    assert paper["year"] == 2015
    assert paper["id"] == "bhfHsCHhomoJ"

    # Test all-in-one call

    papers = scraping.scrape_papers("Autonomous Aerial Water Sampling")
    assert len(papers) > 0
    assert papers[0]["citations"] > 0
    assert papers[0]["year"] == 2015
    assert papers[0]["id"] == "bhfHsCHhomoJ"