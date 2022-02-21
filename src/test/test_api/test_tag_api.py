import sys
sys.path.append("..")

from app.api.models import Tag, Author

def test_crud(client):
    # Create a new tag
    tag1 = Tag('name1')
    resp = client.post('/api/tags', json=tag1.to_dict())
    assert resp.status_code == 201
    t1_id = resp.json['id']

    # Create another tag
    tag2 = Tag('name2')
    resp = client.post('/api/tags', json=tag2.to_dict())
    assert resp.status_code == 201
    t2_id = resp.json['id']

    # Check that both tags were created
    resp = client.get('/api/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    # Check tag1
    resp = client.get(f'/api/tags/{t1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1'

    # Update tag2
    resp = client.put(f'/api/tags/{t2_id}', json={'name': 'name2_updated'})
    assert resp.status_code == 200

    # Check that tag2 was updated
    resp = client.get(f'/api/tags/{t2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2_updated'

    # Delete tag1
    resp = client.delete(f'/api/tags/{t1_id}')
    assert resp.status_code == 200

    # Check that tag1 was deleted
    resp = client.get(f'/api/tags/{t1_id}')
    assert resp.status_code == 404

    resp = client.get('/api/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 1

def test_author_list(client):
    # Create a new tag
    tag1 = Tag('name1')
    resp = client.post('/api/tags', json=tag1.to_dict())
    assert resp.status_code == 201
    t1_id = resp.json['id']

    # Create another tag
    tag2 = Tag('name2')
    resp = client.post('/api/tags', json=tag2.to_dict())
    assert resp.status_code == 201
    t2_id = resp.json['id']

    # Create a new author
    author1 = Author('name1')
    resp = client.post('/api/authors', json=author1.to_dict())
    assert resp.status_code == 201
    a1_id = resp.json['id']

    # Add author1 to tag1
    resp = client.put(f'/api/tags/{t1_id}/authors/{a1_id}')
    assert resp.status_code == 200

    # Check that author1 was added to tag1
    resp = client.get(f'/api/tags/{t1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a1_id

    # Check tag2 has no authors
    resp = client.get(f'/api/tags/{t2_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Remove author1 from tag1
    resp = client.delete(f'/api/tags/{t1_id}/authors/{a1_id}')
    assert resp.status_code == 200
    
    # Check that author1 was removed from tag1
    resp = client.get(f'/api/tags/{t1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 0