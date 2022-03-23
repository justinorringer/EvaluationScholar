import sys
sys.path.append("..")

from backend.api.models import Author, Paper
import pytest

def test_crud(client):
    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/papers', json=paper1.to_dict())

    assert resp.status_code == 201
    p1_id = resp.json['id']

    # Check that the paper was created
    resp = client.get('/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['name'] == 'name1'
    assert resp.json[0]['year'] == 2001

    # Create another paper
    paper2 = Paper('name2', 2002)
    resp = client.post('/papers', json=paper2.to_dict())
    assert resp.status_code == 201
    p2_id = resp.json['id']

    # Check that both papers were created
    resp = client.get('/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    #Check paper1
    resp = client.get(f'/papers/{p1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1'
    assert resp.json['year'] == 2001

    #Check paper2
    resp = client.get(f'/papers/{p2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2'
    assert resp.json['year'] == 2002

    # Update paper1
    resp = client.put(f'/papers/{p1_id}', json={'name': 'name1_updated', 'year': 20011})
    assert resp.status_code == 200

    # Check that paper1 was updated
    resp = client.get(f'/papers/{p1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1_updated'
    assert resp.json['year'] == 20011

    # Partially update paper2
    resp = client.put(f'/papers/{p2_id}', json={'name': 'name2_updated'})
    assert resp.status_code == 200

    # Check that paper2 was partially updated
    resp = client.get(f'/papers/{p2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2_updated'
    assert resp.json['year'] == 2002

    # Delete paper1
    resp = client.delete(f'/papers/{p1_id}')
    assert resp.status_code == 200

    # Check that paper1 was deleted
    resp = client.get(f'/papers/{p1_id}')
    assert resp.status_code == 404

    resp = client.get('/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == p2_id

def test_authors_paper_list(client):
    # Create a new author
    author1 = Author('name1')
    resp = client.post('/authors', json=author1.to_dict())
    a1_id = resp.json['id']

    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/papers', json=paper1.to_dict())
    p1_id = resp.json['id']

    # Check empty paper list
    resp = client.get(f'/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Check empty author list
    resp = client.get(f'/papers/{p1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Add author to paper1
    resp = client.put(f'/papers/{p1_id}/authors/{a1_id}')
    assert resp.status_code == 200

    # Check that author was added
    resp = client.get(f'/papers/{a1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a1_id
    assert resp.json[0]['name'] == 'name1'

    # Add another author to paper1
    author2 = Author('name2')
    resp = client.post('/authors', json=author2.to_dict())
    a2_id = resp.json['id']

    resp = client.put(f'/papers/{p1_id}/authors/{a2_id}')
    assert resp.status_code == 200

    # Check that both authors were added
    resp = client.get(f'/papers/{p1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    # Delete author1
    resp = client.delete(f'/papers/{p1_id}/authors/{a1_id}')
    assert resp.status_code == 200

    # Check that author1 was deleted
    resp = client.get(f'/papers/{p1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a2_id

def test_edge_cases(client):
    # Delete non-existing paper
    resp = client.delete('/papers/1')
    assert resp.status_code == 404

    # Update non-existing paper
    resp = client.put('/papers/1', json={'name': 'name1_updated', 'year': 2001})
    assert resp.status_code == 404

    # Get non-existing paper
    resp = client.get('/papers/1')
    assert resp.status_code == 404

    # Create a new author
    author1 = Author('name1')
    resp = client.post('/authors', json=author1.to_dict())
    a1_id = resp.json['id']

    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/papers', json=paper1.to_dict())
    p1_id = resp.json['id']

    # Delete non-existing author from paper
    resp = client.delete(f'/papers/{p1_id}/authors/{a1_id - 1}')
    assert resp.status_code == 404

    # Add author to non-existing paper
    resp = client.put(f'/papers/{p1_id - 1}/authors/{a1_id}')
    assert resp.status_code == 404

    # Delete author from non-existing paper
    resp = client.delete(f'/papers/{p1_id - 1}/authors/{a1_id}')
    assert resp.status_code == 404

    # Add non-existing author to paper
    resp = client.put(f'/papers/{p1_id}/authors/{a1_id - 1}')
    assert resp.status_code == 404

def test_citations(client):
    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/papers', json=paper1.to_dict())
    p1_id = resp.json['id']

    # Check empty citation list
    resp = client.get(f'/papers/{p1_id}/citations')
    assert resp.status_code == 200
    assert len(resp.json) == 0

@pytest.mark.scraping
def test_scraping(client):
    # Create a new paper
    paper1 = Paper("Autonomous Aerial Water Sampling", 2001)
    resp = client.post('/papers', json=paper1.to_dict())
    p1_id = resp.json['id']
    assert resp.json['latest_citation'] == None

    # Request a citation scrape
    resp = client.post(f'/papers/{p1_id}/citations')
    assert resp.status_code == 200
    c1_id = resp.json['id']

    # Check that there are some citations
    assert resp.json['num_cited'] > 0

    # Check reference
    assert resp.json['paper_id'] == p1_id

    # Check latest citation field
    resp = client.get(f'/papers/{p1_id}')
    assert resp.json['latest_citation']['id'] == c1_id

    # Check citation list route
    resp = client.get(f'/papers/{p1_id}/citations')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == c1_id

    # Check latest citations route
    resp = client.get(f'/papers/{p1_id}/latest-citations')
    assert resp.status_code == 200
    assert resp.json['id'] == c1_id