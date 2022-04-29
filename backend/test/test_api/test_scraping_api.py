import pytest

@pytest.mark.scraping
def test_paper_scraping(client):
    # Scrape a paper
    response = client.get('/scraping/papers?title=Autonomous%20Aerial%20Water%20Sampling')
    assert response.status_code == 200
    assert response.json[0]['citations'] > 0
    assert response.json[0]['year'] == 2015

@pytest.mark.scraping
def test_profile_scraping(client):
    # Scrape a profile
    response = client.get('/scraping/profiles?name=Douglas%20G%20Altman')
    assert response.status_code == 200
    assert response.json[0]['name'] == 'Douglas G Altman'
    assert response.json[0]['institution'] == 'Centre for Statistics in Medicine, University of Oxford'
    assert response.json[0]['id'] == '_QnLm3kAAAAJ'

    response = client.get('/scraping/profiles?name=fajf9ah893fjifjnoa')
    assert response.status_code == 200
    assert len(response.json) == 0

    response = client.get('/scraping/profiles?name=d')
    assert response.status_code == 200
    assert len(response.json) > 5

@pytest.mark.scraping
def test_profile_page_scraping(client):
    response = client.get('/scraping/profiles/0bnFgyAAAAAJ')
    assert response.status_code == 200
    assert response.json['name'] == 'Gregg Rothermel'
    assert len(response.json['papers']) == 100
    assert response.json['papers'][0]['title'] == "Prioritizing test cases for regression testing"
    assert response.json['papers'][0]['year'] == 2001
    assert response.json['papers'][0]['citations'] > 1500

    response = client.get('/scraping/profiles/0bnFgyAAAAAJ?all_papers=true')
    assert response.status_code == 200
    assert response.json['name'] == 'Gregg Rothermel'
    assert len(response.json['papers']) > 200
    assert response.json['papers'][0]['title'] == "Prioritizing test cases for regression testing"