# Move relative imports up a level to be able to access our client
import sys
sys.path.append("..")

from backend.api.models import Issue, AmbiguousPaperIssue

def test_crud(client, session):
    issue = AmbiguousPaperIssue('gid1', 'gid2', 'gid3', 'title1', 'title2', 'title3', 1, 2, 3)
    session.add(issue)
    session.commit()

    assert session.query(AmbiguousPaperIssue).count() == 1

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['gid_1'] == 'gid1'
    assert resp.json[0]['gid_2'] == 'gid2'
    assert resp.json[0]['type'] == 'ambiguous_paper_issue'
    assert resp.json[0]['id'] == issue.id

    resp = client.get(f'/issues/{issue.id}')
    assert resp.status_code == 200
    assert resp.json['gid_1'] == 'gid1'
    assert resp.json['id'] == issue.id

    resp = client.get(f'/issues/{issue.id + 1}')
    assert resp.status_code == 404

    session.delete(issue)
    session.commit()

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 0