import sys
sys.path.append("..")

from backend.api.models import Tag, Author

def test_crud(client):
    # Create a new tag
    tag1 = Tag('name1')
    resp = client.post('/tags', json=tag1.to_dict())
    assert resp.status_code == 201
    t1_id = resp.json['id']

    # Create another tag
    tag2 = Tag('name2')
    resp = client.post('/tags', json=tag2.to_dict())
    assert resp.status_code == 201
    t2_id = resp.json['id']

    # Check that both tags were created
    resp = client.get('/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    # Check tag1
    resp = client.get(f'/tags/{t1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1'

    # Update tag2
    resp = client.put(f'/tags/{t2_id}', json={'name': 'name2_updated'})
    assert resp.status_code == 200

    # Check that tag2 was updated
    resp = client.get(f'/tags/{t2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2_updated'

    # Delete tag1
    resp = client.delete(f'/tags/{t1_id}')
    assert resp.status_code == 200

    # Check that tag1 was deleted
    resp = client.get(f'/tags/{t1_id}')
    assert resp.status_code == 404

    resp = client.get('/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 1

def test_author_list(client):
    # Create a new tag
    tag1 = Tag('name1')
    resp = client.post('/tags', json=tag1.to_dict())
    assert resp.status_code == 201
    t1_id = resp.json['id']

    # Create another tag
    tag2 = Tag('name2')
    resp = client.post('/tags', json=tag2.to_dict())
    assert resp.status_code == 201
    t2_id = resp.json['id']

    # Create a new author
    author1 = Author('name1', 'q1236AG15KB7')
    resp = client.post('/authors', json=author1.to_dict())
    assert resp.status_code == 201
    a1_id = resp.json['id']

    # Add author1 to tag1
    resp = client.put(f'/tags/{t1_id}/authors/{a1_id}')
    assert resp.status_code == 200

    # Check that author1 was added to tag1
    resp = client.get(f'/tags/{t1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a1_id

    # Check tag2 has no authors
    resp = client.get(f'/tags/{t2_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Remove author1 from tag1
    resp = client.delete(f'/tags/{t1_id}/authors/{a1_id}')
    assert resp.status_code == 200
    
    # Check that author1 was removed from tag1
    resp = client.get(f'/tags/{t1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 0

def test_batch(client):
    tag_ids = []
    for i in range(10):
        tag = Tag(f'name{i}')
        resp = client.post('/tags', json=tag.to_dict())
        assert resp.status_code == 201
        tag_ids.append(resp.json['id'])
    
    author_ids = []
    for i in range(10):
        author = Author(f'name{i}', f'scholar_id{i}')
        resp = client.post('/authors', json=author.to_dict())
        assert resp.status_code == 201
        author_ids.append(resp.json['id'])
    
    # Add authors to tags
    add_tag_list = list(map(lambda x: tag_ids[x], [0, 3, 6, 7]))
    add_author_list = list(map(lambda x: author_ids[x], [0, 1, 2, 3]))

    client.put('/tags/authors', json={'tags': add_tag_list, 'authors': add_author_list})

    # Check that authors were added to tags
    for tag_id in tag_ids:
        resp = client.get(f'/tags/{tag_id}/authors')
        assert resp.status_code == 200

        if tag_id in add_tag_list:
            assert len(resp.json) == 4

            # Check each author
            for author_id in add_author_list:
                assert author_id in [a['id'] for a in resp.json]
        else:
            assert len(resp.json) == 0

    # Remove authors from tags
    remove_tag_list = list(map(lambda x: tag_ids[x], [0, 1, 3]))
    remove_author_list = list(map(lambda x: author_ids[x], [0, 1]))

    client.delete('/tags/authors', json={'tags': remove_tag_list, 'authors': remove_author_list})

    # Check that authors were removed from tags
    resp = client.get(f'/tags/{tag_ids[0]}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    resp = client.get(f'/tags/{tag_ids[3]}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    resp = client.get(f'/tags/{tag_ids[6]}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 4

    resp = client.get(f'/tags/{tag_ids[4]}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 0