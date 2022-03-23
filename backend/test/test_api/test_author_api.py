# Move relative imports up a level to be able to access our client
import sys
sys.path.append("..")

from backend.api.models import Author, Paper, Tag

def test_crud(client):
    # Create a new author
    author1 = Author('name1', 'q1124AA12BD4')
    resp = client.post('/authors', json=author1.to_dict())

    assert resp.status_code == 201
    a1_id = resp.json['id']

    # Check that the author was created
    resp = client.get('/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['name'] == 'name1'
    assert resp.json[0]['scholar_id'] == 'q1124AA12BD4'

    # Create another author
    author2 = Author('name2', 'q1364BT15HD4')
    resp = client.post('/authors', json=author2.to_dict())
    assert resp.status_code == 201
    a2_id = resp.json['id']

    # Check that both authors were created
    resp = client.get('/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    #Check author1
    resp = client.get(f'/authors/{a1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1'

    #Check author2
    resp = client.get(f'/authors/{a2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2'

    # Update author1
    resp = client.put(f'/authors/{a1_id}', json={'name': 'name1_updated', 'scholar_id': 'q1376BY15UD4'})
    assert resp.status_code == 200

    # Check that author1 was updated
    resp = client.get(f'/authors/{a1_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name1_updated'
    assert resp.json['scholar_id'] == 'q1376BY15UD4'


    # Partially update author2
    resp = client.put(f'/authors/{a2_id}', json={'name': 'name2_updated'})
    assert resp.status_code == 200

    # Check that author2 was partially updated
    resp = client.get(f'/authors/{a2_id}')
    assert resp.status_code == 200
    assert resp.json['name'] == 'name2_updated'

    # Delete author1
    resp = client.delete(f'/authors/{a1_id}')
    assert resp.status_code == 200

    # Check that author1 was deleted
    resp = client.get(f'/authors/{a1_id}')
    assert resp.status_code == 404

    resp = client.get('/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a2_id

def test_paper_list(client):
    # Create a new author
    author1 = Author('name1', 'q1236AG15KB7')
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

    # Add paper to author1
    resp = client.put(f'/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 200

    # Check that paper was added
    resp = client.get(f'/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == p1_id
    assert resp.json[0]['name'] == 'name1'
    assert resp.json[0]['year'] == 2001

    # Add another paper to author1
    paper2 = Paper('name2', 2002)
    resp = client.post('/papers', json=paper2.to_dict())
    p2_id = resp.json['id']

    resp = client.put(f'/authors/{a1_id}/papers/{p2_id}')
    assert resp.status_code == 200

    # Check that both papers were added
    resp = client.get(f'/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    # Delete paper1
    resp = client.delete(f'/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 200

    # Check that paper1 was deleted
    resp = client.get(f'/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == p2_id

def test_edge_cases(client):
    # Delete non-existing author
    resp = client.delete('/authors/1')
    assert resp.status_code == 404

    # Update non-existing author
    resp = client.put('/authors/1', json={'name': 'name1_updated'})
    assert resp.status_code == 404

    # Get non-existing author
    resp = client.get('/authors/1')
    assert resp.status_code == 404

    # Create a new author
    author1 = Author('name1', 'q1236AG15KB7')
    resp = client.post('/authors', json=author1.to_dict())
    a1_id = resp.json['id']

    # Create a new paper
    paper1 = Paper('name1', 2001)
    resp = client.post('/papers', json=paper1.to_dict())
    p1_id = resp.json['id']

    # Delete non-existing paper from author
    resp = client.delete(f'/authors/{a1_id}/papers/{p1_id - 1}')
    assert resp.status_code == 404

    # Add paper to non-existing author
    resp = client.put(f'/authors/{a1_id - 1}/papers/{p1_id}')
    assert resp.status_code == 404

    # Delete paper from non-existing author
    resp = client.delete(f'/authors/{a1_id - 1}/papers/{p1_id}')
    assert resp.status_code == 404

    # Add non-existing paper to author
    resp = client.put(f'/authors/{a1_id}/papers/{p1_id - 1}')
    assert resp.status_code == 404

def test_tag_list(client):
    # Create a new author
    author1 = Author('name1', 'q1236AG15KB7')
    resp = client.post('/authors', json=author1.to_dict())
    assert resp.status_code == 201
    a1_id = resp.json['id']

    # Create a new tag
    tag1 = Tag('name1')
    resp = client.post('/tags', json=tag1.to_dict())
    assert resp.status_code == 201
    t1_id = resp.json['id']

    # Check empty tag list
    resp = client.get(f'/authors/{a1_id}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Add tag to author1
    resp = client.put(f'/authors/{a1_id}/tags/{t1_id}')
    assert resp.status_code == 200

    # Check that tag was added
    resp = client.get(f'/authors/{a1_id}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == t1_id

    # Check the tag's author list
    resp = client.get(f'/tags/{t1_id}/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == a1_id

    # Remove tag from author1
    resp = client.delete(f'/authors/{a1_id}/tags/{t1_id}')
    assert resp.status_code == 200

    # Check that tag was removed
    resp = client.get(f'/authors/{a1_id}/tags')
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
    
    # Add tags to authors
    add_tag_list = list(map(lambda x: tag_ids[x], [1, 3, 4, 5, 6]))
    add_author_list = list(map(lambda x: author_ids[x], [5, 6, 4, 2]))

    client.put('/authors/tags', json={'tags': add_tag_list, 'authors': add_author_list})

    # Check that tags were added to authors
    for author_id in author_ids:
        resp = client.get(f'/authors/{author_id}/tags')
        assert resp.status_code == 200

        if author_id in add_author_list:
            assert len(resp.json) == 5

            for tag_id in add_tag_list:
                assert tag_id in [t['id'] for t in resp.json]
        else:
            assert len(resp.json) == 0
    
    # Remove tags from authors
    remove_tag_list = list(map(lambda x: tag_ids[x], [0, 1, 3]))
    remove_author_list = list(map(lambda x: author_ids[x], [5, 6]))

    client.delete('/authors/tags', json={'tags': remove_tag_list, 'authors': remove_author_list})

    # Check that tags were removed from authors
    resp = client.get(f'/authors/{author_ids[5]}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 3

    resp = client.get(f'/authors/{author_ids[6]}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 3

    resp = client.get(f'/authors/{author_ids[4]}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 5

    resp = client.get(f'/authors/{author_ids[0]}/tags')
    assert resp.status_code == 200
    assert len(resp.json) == 0