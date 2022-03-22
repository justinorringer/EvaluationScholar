import sys
sys.path.append("..")

from backend.api.models import Task, CreatePaperTask, UpdateCitationsTask, Paper

def test_read(client, session):
    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    task1 = CreatePaperTask("title", "author")
    session.add(task1)
    session.commit()

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'create_paper_task'

    paper = Paper("title", 2000)
    session.add(paper)
    session.flush()

    task2 = UpdateCitationsTask(paper.id)
    session.add(task2)
    session.commit()

    resp = client.get('/tasks?type=create_paper_task')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'create_paper_task'
    print(resp.json)

    resp = client.get('/tasks?type=update_citations_task')
    assert resp.status_code == 200
    assert len(resp.json) == 1
    assert resp.json[0]['type'] == 'update_citations_task'
    print(resp.json)

    resp = client.get('/tasks?type=invalid_type')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 2

    resp = client.get(f'/tasks/{task2.id}')
    assert resp.status_code == 200
    assert resp.json['type'] == 'update_citations_task'

def test_delete(client, session):
    task1 = CreatePaperTask("title", "author")
    session.add(task1)
    session.commit()

    resp = client.delete(f'/tasks/{task1.id}')
    assert resp.status_code == 200

    resp = client.delete(f'/tasks/{task1.id}')
    assert resp.status_code == 404

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    paper = Paper("title", 2000)
    session.add(paper)
    session.flush()

    task2 = UpdateCitationsTask(paper.id)
    task3 = CreatePaperTask("title", "author")
    task4 = CreatePaperTask("title", "author")
    task5 = UpdateCitationsTask(paper.id)

    session.add(task2)
    session.add(task3)
    session.add(task4)
    session.add(task5)
    session.commit()

    resp = client.delete(f'/tasks/{task2.id}')
    assert resp.status_code == 200

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 3

    resp = client.delete('/tasks?type=create_paper_task')
    assert resp.status_code == 200

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 1

    task6 = CreatePaperTask("title", "author")
    session.add(task6)
    session.commit()

    resp = client.delete('/tasks')
    assert resp.status_code == 200

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 0