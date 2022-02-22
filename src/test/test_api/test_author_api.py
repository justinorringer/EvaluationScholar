# Move relative imports up a level to be able to access our client
import sys
sys.path.append("..")

from app.api.models import Author, Paper, Tag

def test_crud(client):
    # Create a new author
    author1 = Author('name1')
    resp = client.post('/api/authors', json=author1.to_dict())

    assert resp.status_code == 201
    a1_id = resp.json['id']

    # Check that the author was created
    resp = client.get('/api/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['name'] == 'name1'

    # Create another author
    author2 = Author('name2')
    resp = client.post('/api/authors', json=author2.to_dict())
    assert resp.status_code == 201
    a2_id = resp.json['id']

    # Check that both authors were created
    resp = client.get('/api/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    #Check author1
    resp = client.get(f'/api/authors/{a1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1'

    #Check author2
    resp = client.get(f'/api/authors/{a2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2'

    # Update author1
    resp = client.put(f'/api/authors/{a1_id}', json={'name': 'name1_updated'})
    assert resp.status_code == 200

    # Check that author1 was updated
    resp = client.get(f'/api/authors/{a1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1_updated'


    # Partially update author2
    resp = client.put(f'/api/authors/{a2_id}', json={'name': 'name2_updated'})
    assert resp.status_code == 200

    # Check that author2 was partially updated
    resp = client.get(f'/api/authors/{a2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2_updated'

    # Delete author1
    resp = client.delete(f'/api/authors/{a1_id}')
    assert resp.status_code == 200

    # Check that author1 was deleted
    resp = client.get(f'/api/authors/{a1_id}')
    assert resp.status_code == 404

    resp = client.get('/api/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a2_id

def test_paper_list(client):
    # Create a new author
    author1 = Author('name1')
    resp = client.post('/api/authors', json=author1.to_dict())
    a1_id = resp.json['id']

    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/api/papers', json=paper1.to_dict())
    p1_id = resp.json['id']

    # Check empty paper list
    resp = client.get(f'/api/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Add paper to author1
    resp = client.put(f'/api/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 200

    # Check that paper was added
    resp = client.get(f'/api/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == p1_id
    assert resp.json[0]['name'] == 'name1'
    assert resp.json[0]['year'] == 2001

    # Add another paper to author1
    paper2 = Paper('name2', 2002)
    resp = client.post('/api/papers', json=paper2.to_dict())
    p2_id = resp.json['id']

    resp = client.put(f'/api/authors/{a1_id}/papers/{p2_id}')
    assert resp.status_code == 200

    # Check that both papers were added
    resp = client.get(f'/api/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    # Delete paper1
    resp = client.delete(f'/api/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 200

    # Check that paper1 was deleted
    resp = client.get(f'/api/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == p2_id

def test_edge_cases(client):
    # Delete non-existing author
    resp = client.delete('/api/authors/1')
    assert resp.status_code == 404

    # Update non-existing author
    resp = client.put('/api/authors/1', json={'name': 'name1_updated'})
    assert resp.status_code == 404

    # Get non-existing author
    resp = client.get('/api/authors/1')
    assert resp.status_code == 404

    # Create a new author
    author1 = Author('name1')
    resp = client.post('/api/authors', json=author1.to_dict())
    a1_id = resp.json['id']

    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/api/papers', json=paper1.to_dict())
    p1_id = resp.json['id']

    # Delete non-existing paper from author
    resp = client.delete(f'/api/authors/{a1_id}/papers/{p1_id - 1}')
    assert resp.status_code == 404

    # Add paper to non-existing author
    resp = client.put(f'/api/authors/{a1_id - 1}/papers/{p1_id}')
    assert resp.status_code == 404

    # Delete paper from non-existing author
    resp = client.delete(f'/api/authors/{a1_id - 1}/papers/{p1_id}')
    assert resp.status_code == 404

    # Add non-existing paper to author
    resp = client.put(f'/api/authors/{a1_id}/papers/{p1_id - 1}')
    assert resp.status_code == 404

def test_tag_list(client):
    # Create a new author
    author1 = Author('name1')
    resp = client.post('/api/authors', json=author1.to_dict())
    assert resp.status_code == 201
    a1_id = resp.json['id']

    # Create a new tag
    tag1 = Tag('name1')
    resp = client.post('/api/tags', json=tag1.to_dict())
    assert resp.status_code == 201
    t1_id = resp.json['id']

    # Check empty tag list
    resp = client.get(f'/api/authors/{a1_id}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Add tag to author1
    resp = client.put(f'/api/authors/{a1_id}/tags/{t1_id}')
    assert resp.status_code == 200

    # Check that tag was added
    resp = client.get(f'/api/authors/{a1_id}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == t1_id

    # Check the tag's author list
    resp = client.get(f'/api/tags/{t1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a1_id

    # Remove tag from author1
    resp = client.delete(f'/api/authors/{a1_id}/tags/{t1_id}')
    assert resp.status_code == 200

    # Check that tag was removed
    resp = client.get(f'/api/authors/{a1_id}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 0
