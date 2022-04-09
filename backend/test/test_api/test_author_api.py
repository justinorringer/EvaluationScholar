# Move relative imports up a level to be able to access our client
from datetime import datetime, timedelta
import sys
sys.path.append("..")

from backend.api.models import Author, Paper, Tag, Citation

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

def test_paper_list(client, session):
    # Create a new author
    author1 = Author('name1', 'q1236AG15KB7')
    resp = client.post('/authors', json=author1.to_dict())
    a1_id = resp.json['id']

    # Create a new paper
    paper1 = Paper('name1', 2001)
    session.add(paper1)
    session.commit()
    p1_id = paper1.id

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

    resp = client.get(f'/authors/{a1_id}?include=papers')
    assert resp.status_code == 200
    assert len(resp.json['papers']) == 2
    assert resp.json['papers'][0]['id'] == p1_id
    assert resp.json['papers'][0]['latest_citation'] == None

    paper1.citations.append(Citation(367, datetime.now()))
    paper1.citations.append(Citation(368, datetime.now() + timedelta(days=1)))
    session.commit()

    resp = client.get(f'/authors/{a1_id}?include=papers')
    assert resp.status_code == 200
    assert len(resp.json['papers']) == 2
    assert resp.json['papers'][0]['id'] == p1_id
    assert resp.json['papers'][0]['latest_citation']['num_cited'] == 368
    assert resp.json['papers'][1]['id'] == p2_id
    assert resp.json['papers'][1]['latest_citation'] == None

    # Delete paper1
    resp = client.delete(f'/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 200

    # Check that paper1 was deleted
    resp = client.get(f'/authors/{a1_id}/papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == p2_id

    resp = client.get(f'/authors/{a1_id}?include=papers')
    assert resp.status_code == 200
    assert len(resp.json['papers']) == 1
    assert resp.json['papers'][0]['id'] == p2_id
    assert resp.json['papers'][0]['latest_citation'] == None

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

    # Add author with missing name
    resp = client.post('/authors', json={'scholar_id': 'q1236AG15KB7'})
    assert resp.status_code == 400

    # Duplicate scholar id
    resp = client.post('/authors', json={'name': 'name2', 'scholar_id': 'q1236AG15KB8'})
    assert resp.status_code == 201

    resp = client.post('/authors', json={'name': 'name2', 'scholar_id': 'q1236AG15KB8'})
    assert resp.status_code == 400

    # Add author to paper twice
    resp = client.put(f'/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 200

    resp = client.put(f'/authors/{a1_id}/papers/{p1_id}')
    assert resp.status_code == 400

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

def test_filtering(client, session):
    # Create some test tags
    tag_ids = []
    for i in range(5):
        tag = Tag(f'name{i}')
        resp = client.post('/tags', json=tag.to_dict())
        assert resp.status_code == 201
        tag_ids.append(resp.json['id'])
    
    # Create some test authors
    author_ids = []
    authors = []
    names = ["arthur ryAn", "molly undore", "sandra DolloP", "clarice OrAnge", "paul goRbovdo"]
    for i in range(5):
        author = Author(names[i], f'scholar_id{i}')
        session.add(author)
        session.flush()
        author_ids.append(author.id)
        authors.append(author)
    
    session.commit()

    citation_counts = [[5, 6, 0, 2], [12, 0, 99, 3, 5, 6], [8, 9, 34, 6, 7, 112], [1, 2, 1, 0], [0, 10]]
    for i in range(5):
        for j, citation_count in enumerate(citation_counts[i]):
            paper = Paper(f'paper{i} {j}', 2000)
            paper.citations.append(Citation(citation_count, datetime.now()))
            authors[i].papers.append(paper)
    
    session.commit()
    
    a_t = lambda x: list(map(lambda y: author_ids[y], x))
    t_t = lambda x: list(map(lambda y: tag_ids[y], x))

    # Add tags to authors
    client.put('/authors/tags', json={'tags': t_t([0]), 'authors': a_t([0, 1, 2, 3])})
    client.put('/authors/tags', json={'tags': t_t([1]), 'authors': a_t([0, 1, 4])})
    client.put('/authors/tags', json={'tags': t_t([2]), 'authors': a_t([2, 3, 4])})
    client.put('/authors/tags', json={'tags': t_t([3]), 'authors': a_t([1, 2])})
    client.put('/authors/tags', json={'tags': t_t([4]), 'authors': a_t([0, 2, 3])})

    # Test some filtering
    resp = client.get('/authors?name=pa')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == author_ids[4]

    resp = client.get('/authors?name=ol')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    resp = client.get(f'/authors?tags={tag_ids[1]}')
    assert resp.status_code == 200
    assert len(resp.json) == 3
    assert author_ids[0] in [a['id'] for a in resp.json]
    assert author_ids[1] in [a['id'] for a in resp.json]
    assert author_ids[4] in [a['id'] for a in resp.json]

    resp = client.get(f'/authors?tags={tag_ids[0]}')
    assert resp.status_code == 200
    assert len(resp.json) == 4

    resp = client.get(f'/authors?tags={tag_ids[0]},{tag_ids[1]}')
    assert resp.status_code == 200
    assert len(resp.json) == 2
    assert author_ids[0] in [a['id'] for a in resp.json]
    assert author_ids[1] in [a['id'] for a in resp.json]

    resp = client.get(f'/authors?tags={tag_ids[0]},{tag_ids[1]},{tag_ids[2]}')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    resp = client.get(f'/authors?tags={tag_ids[0]}&name=do')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    resp = client.get(f'/authors?tags={tag_ids[0]}&name=ul')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    resp = client.get(f'/authors?name=ol sa')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    resp = client.get('/authors?name=Sandra Dollop')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    # Values for the test authors:
    # h-index   i10-index
    # 2         0
    # 4         2
    # 6         2
    # 1         0
    # 1         1

    resp = client.get('/authors?min-h=2&max-i10=1')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    resp = client.get('/authors?max-h=3&min-i10=1')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    resp = client.get('/authors?min-h=2')
    assert resp.status_code == 200
    assert len(resp.json) == 3

    resp = client.get('/authors?min-i10=1&max-i10=1&min-h=1')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    resp = client.get('/authors?max-h=5&min-i10=1')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    resp = client.get('/authors?max-h=5&min-i10=1&name=und')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    authors[0].papers.append(Paper('paper_no_citations', 2000))
    session.commit()

    resp = client.get('/authors?min-h=2&max-i10=1')
    assert resp.status_code == 200
    assert len(resp.json) == 1

def test_include(client, session):
    author = Author('arthur ryAn', 'scholar_id')
    session.add(author)

    paper = Paper('paper', 2000)
    paper.scholar_id = 'scholar_id'
    paper.citations.append(Citation(5, datetime.now()))
    author.papers.append(paper)

    tag = Tag('name')
    author.tags.append(tag)
    
    session.commit()

    resp = client.get('/authors')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == author.id
    assert 'tags' not in resp.json[0]
    assert 'papers' not in resp.json[0]

    resp = client.get('/authors?include=tags')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == author.id
    assert 'tags' in resp.json[0]
    assert resp.json[0]['tags'][0]['name'] == tag.name
    assert resp.json[0]['tags'][0]['id'] == tag.id
    assert 'papers' not in resp.json[0]

    resp = client.get('/authors?include=papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['id'] == author.id
    assert 'tags' not in resp.json[0]
    assert 'papers' in resp.json[0]
    assert resp.json[0]['papers'][0]['id'] == paper.id
    assert resp.json[0]['papers'][0]['latest_citation']['num_cited'] == paper.citations[0].num_cited
    assert resp.json[0]['papers'][0]['year'] == paper.year
    assert resp.json[0]['papers'][0]['name'] == paper.name
    assert resp.json[0]['papers'][0]['scholar_id'] == paper.scholar_id

    resp = client.get('/authors?include=tags,papers')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert 'tags' in resp.json[0]
    assert 'papers' in resp.json[0]
    assert len(resp.json[0]['tags']) == 1
    assert len(resp.json[0]['papers']) == 1