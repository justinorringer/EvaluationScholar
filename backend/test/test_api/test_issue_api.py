# Move relative imports up a level to be able to access our client
import sys
sys.path.append("..")

from backend.api.models import Issue, AmbiguousPaperIssue, Paper

def test_crud(client, session):
    paper_1 = Paper("paper1", 2001)
    paper_2 = Paper("paper2", 2002)
    paper_3 = Paper("paper3", 2003)

    resp = client.post('/papers', json=paper_1.to_dict())
    assert resp.status_code == 201
    paper_1_id = resp.json['id']

    resp = client.post('/papers', json=paper_2.to_dict())
    assert resp.status_code == 201
    paper_2_id = resp.json['id']

    resp = client.post('/papers', json=paper_3.to_dict())
    assert resp.status_code == 201
    paper_3_id = resp.json['id']

    issue = AmbiguousPaperIssue(author_name="author", paper_id_1=paper_1_id, paper_id_2=paper_2_id, paper_id_3=paper_3_id)
    session.add(issue)
    session.commit()

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'ambiguous_paper_issue'
    assert resp.json[0]['author_name'] == 'author'
    assert resp.json[0]['paper_1']['id'] == paper_1_id
    assert resp.json[0]['paper_1']['year'] == 2001
    assert resp.json[0]['paper_2']['name'] == 'paper2'

    resp = client.get(f'/issues/{issue.id}')
    assert resp.status_code == 200
    assert resp.json['type'] == 'ambiguous_paper_issue'
    assert resp.json['author_name'] == 'author'

    resp = client.delete(f'/issues/{issue.id}')
    assert resp.status_code == 200

    resp = client.get(f'/issues/{issue.id}')
    assert resp.status_code == 404

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    issue2 = AmbiguousPaperIssue('author', paper_1_id, paper_2_id)
    session.add(issue2)
    session.commit()

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'ambiguous_paper_issue'
    assert resp.json[0]['author_name'] == 'author'
    assert resp.json[0]['paper_1']['name'] == 'paper1'
    assert resp.json[0]['paper_1']['year'] == 2001
    assert resp.json[0]['paper_2']['name'] == 'paper2'