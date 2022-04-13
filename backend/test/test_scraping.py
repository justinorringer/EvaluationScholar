import backend.scraping as scraping
import backend.scraping.scraperapi as scraperapi
import backend.scraping.google_scholar as google_scholar
import pytest

@pytest.mark.scraping
def test_profiles():
    #Test Google Scholar searching and parsing

    html = google_scholar.get_profile_search_html("douglas G altman")
    profile_blocks = google_scholar.parse_profile_blocks(html)
    assert len(profile_blocks) > 0
    
    profile_block = profile_blocks[0]
    profile = google_scholar.parse_profile(profile_block)

    name = google_scholar.parse_profile_name(profile_block)
    assert name == "Douglas G Altman"

    institution = google_scholar.parse_profile_institution(profile_block)
    assert institution == "Centre for Statistics in Medicine, University of Oxford"

    id = google_scholar.parse_profile_id(profile_block)
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
def test_zero_citations():
    html = google_scholar.get_paper_search_html("ITALIAN OCCUPATION OF ETHIOPIA.-FRONTIER QUESTIONS: OCCUPATION OF POST NORTH OF KOKOI.")

    paper_blocks = google_scholar.parse_paper_blocks(html)
    assert len(paper_blocks) > 0

    paper_block = paper_blocks[0]
    paper = google_scholar.parse_paper(paper_block)

    assert paper['citations'] == 0
    assert paper['year'] == 1938
    assert paper['title'] == "ITALIAN OCCUPATION OF ETHIOPIA.-FRONTIER QUESTIONS: OCCUPATION OF POST NORTH OF KOKOI."
    assert paper['id'] == "Mu4Snx7skzcJ"
    assert len(paper['authors']) == 0

@pytest.mark.scraping
def test_papers():
    # Test Google Scholar searching and parsing

    html = google_scholar.get_paper_search_html("Autonomous Aerial Water Sampling")

    paper_blocks = google_scholar.parse_paper_blocks(html)
    assert len(paper_blocks) >= 3

    papers = [google_scholar.parse_paper(paper_block) for paper_block in paper_blocks]

    # There should be a normal paper entry in the list
    assert len([paper for paper in papers if "citation_entry" not in paper]) >=1 
    normal_paper = [paper for paper in papers if 'citation_entry' not in paper][0]

    assert normal_paper["citations"] > 0
    assert normal_paper["year"] == 2015
    assert normal_paper["id"] == "bhfHsCHhomoJ"
    assert normal_paper["title"].lower() == "Autonomous Aerial Water Sampling".lower()
    assert len(normal_paper["authors"]) == 3
    assert 'citation_entry' not in normal_paper

    # There should be some citation entries
    assert len([paper for paper in papers if 'citation_entry' in paper]) >= 2
    # Make sure the title is being gathered correctly
    assert len([paper for paper in papers if 'citation_entry' in paper and paper['title'] == "Autonomous aerial water sampling. J Field Robot 32 (8): 1095–1113"]) == 1

    # Find the paper block for the normal paper
    normal_paper_block = paper_blocks[papers.index(normal_paper)]
    # Test parsing on its own
    assert google_scholar.parse_citations(normal_paper_block) > 0
    assert google_scholar.parse_year(normal_paper_block) == 2015
    assert google_scholar.parse_paper_id(normal_paper_block) == "bhfHsCHhomoJ"
    assert google_scholar.parse_title(normal_paper_block).lower() == "Autonomous Aerial Water Sampling".lower()

    # Check the scraped authors
    authors = google_scholar.parse_paper_authors(normal_paper_block)
    assert {'name': 'JP Ore', 'id': 'q7jnx5IAAAAJ'} in authors
    assert {'name': 'S Elbaum', 'id': 'swPW5FYAAAAJ'} in authors
    assert {'name': 'A Burgin', 'id': 'mesiHAsAAAAJ'} in authors

    # Test all-in-one call
    searched_papers = google_scholar.search_papers("Autonomous Aerial Water Sampling")
    assert len(searched_papers) > 0
    s_paper = searched_papers[0]

    # There shouldn't be citation entries from this call
    assert len([s_paper for s_paper in searched_papers if 'citation_entry' in s_paper]) == 0

    # Test the values
    assert s_paper["citations"] > 0
    assert s_paper["year"] == 2015
    assert s_paper["id"] == "bhfHsCHhomoJ"

    # Make sure merging works. The citation entries should be merged into the normal paper entry, so the count will be higher
    assert s_paper['citations'] > normal_paper['citations']