# Move relative imports up a level to be able to access our client
import sys
sys.path.append("..")

import pytest
from backend.api.models import CreatePaperTask, Issue, AmbiguousPaperIssue, Paper, AmbiguousPaperChoice, Author, UpdateCitationsTask
from backend.test import wait_for_task, wait_for_task_count

def test_crud(client, session):
    author = Author(name="author", scholar_id="_QnLm3kAAAAJ")
    session.add(author)
    session.flush()

    issue = AmbiguousPaperIssue(author.id, "lava")
    session.add(issue)
    session.flush()

    choice_1 = AmbiguousPaperChoice("The dynamics of lava flows", 2000, "N-GznIQELfYJ", 10, issue.id, [])
    choice_2 = AmbiguousPaperChoice("Lava effusion rate definition and measurement: a review", 2001, "MVNZ5BM8UegJ", 20, issue.id, [])
    choice_3 = AmbiguousPaperChoice("Differentiation behavior of Kilauea Iki lava lake, Kilauea Volcano, Hawaii: an overview of past and current work", 2002, "cy0qh3krAjgJ", 30, issue.id, [])

    session.add(choice_1)
    session.add(choice_2)
    session.add(choice_3)
    session.commit()

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'ambiguous_paper_issue'
    assert resp.json[0]['id'] == issue.id

    assert len(resp.json[0]['paper_choices']) == 3
    assert resp.json[0]['paper_choices'][0]['name'] == 'The dynamics of lava flows'
    assert resp.json[0]['paper_choices'][0]['year'] == 2000
    assert resp.json[0]['paper_choices'][0]['scholar_id'] == 'N-GznIQELfYJ'
    assert resp.json[0]['paper_choices'][0]['citations'] == 10

    assert resp.json[0]['author']['name'] == 'author'
    assert resp.json[0]['author']['id'] == author.id

    resp = client.get(f'/issues/{issue.id}')
    assert resp.status_code == 200
    assert resp.json['type'] == 'ambiguous_paper_issue'
    assert resp.json['id'] == issue.id

    resp = client.delete(f'/issues/{issue.id}')
    assert resp.status_code == 200

    resp = client.get(f'/issues/{issue.id}')
    assert resp.status_code == 404

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    issue2 = AmbiguousPaperIssue(author.id, "title_query")
    session.add(issue2)
    session.commit()

    resp = client.get('/issues')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'ambiguous_paper_issue'
    assert resp.json[0]['id'] == issue2.id

@pytest.mark.scraping
def test_ambiguous_resolve(client, session, task_manager):
    author = Author("author", "fhnifdsa")
    session.add(author)
    session.flush()

    issue = AmbiguousPaperIssue(author.id, "lava")
    session.add(issue)
    session.flush()

    choice_1 = AmbiguousPaperChoice("The dynamics of lava flows", 2000, "N-GznIQELfYJ", 10, issue.id, [])
    choice_2 = AmbiguousPaperChoice("Lava effusion rate definition and measurement: a review", 2001, "MVNZ5BM8UegJ", 20, issue.id, [])
    choice_3 = AmbiguousPaperChoice("Differentiation behavior of Kilauea Iki lava lake, Kilauea Volcano, Hawaii: an overview of past and current work", 2002, "cy0qh3krAjgJ", 30, issue.id, [])

    session.add(choice_1)
    session.add(choice_2)
    session.add(choice_3)
    session.commit()

    task_manager.disable()

    resp = client.post(f'/issues/{issue.id}/resolve', json={'correct_scholar_id': 'MVNZ5BM8UegJ'})
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'

    assert session.query(CreatePaperTask).count() == 1
    task = session.query(CreatePaperTask).first()

    task_manager.enable()

    wait_for_task(task_manager, task.id)

    assert session.query(Paper).count() == 1
    paper = session.query(Paper).first()
    assert paper.name == 'Lava effusion rate definition and measurement: a review'
    assert paper.year == 2007
    assert paper.scholar_id == 'MVNZ5BM8UegJ'

    assert session.query(UpdateCitationsTask).count() == 1