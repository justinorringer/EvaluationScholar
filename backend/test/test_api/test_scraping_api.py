def test_scraping(client):
    # Scrape a paper
    response = client.get('/scraping/papers?title=Autonomous%20Aerial%20Water%20Sampling')
    assert response.status_code == 200
    assert response.json['citation_count'] > 0
    assert response.json['year'] == 2015