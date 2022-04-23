import io
import os
import sys
sys.path.append("..")

from backend.api.models import Author, Task, CreatePaperTask, UpdateCitationsTask, Paper

def test_read(client, session):
    author = Author('JP Ore', 'q1124AA12BD4')
    session.add(author)
    session.flush()

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    task1 = CreatePaperTask("title", author.id)
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
    assert resp.json[0]['author']['name'] == 'JP Ore'
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
    author = Author('JP Ore', 'q1124AA12BD4')
    session.add(author)
    session.flush()

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
    task3 = CreatePaperTask("title", author.id)
    task4 = CreatePaperTask("title", author.id)
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

    task6 = CreatePaperTask("title", author.id)
    session.add(task6)
    session.commit()

    resp = client.delete('/tasks')
    assert resp.status_code == 200

    resp = client.get('/tasks')
    assert resp.status_code == 200
    assert len(resp.json) == 0

def test_create(client):
    author = Author('JP Ore', 'q1124AA12BD4')
    resp = client.post('/authors', json=author.to_dict())
    author_id = resp.json['id']
    assert resp.json['uploaded_papers'] == False

    data = dict(
        file = io.open(f'{os.getcwd()}/test/test_files/Ore.txt', 'rb', buffering=0)
    )
    
    resp = client.post(f'/tasks/create-papers?author_id={author_id}', data=data, content_type='multipart/form-data')
    assert resp.status_code == 201
    assert len(resp.json) == 16

    resp = client.get(f'/authors/{author_id}')
    assert resp.json['uploaded_papers'] == True

    # Test invalid author
    data = dict(
        file = io.open(f'{os.getcwd()}/test/test_files/Ore.txt', 'rb', buffering=0)
    )
    resp = client.post('/tasks/create-papers?author_id=invalid_id', data=data, content_type='multipart/form-data')
    assert resp.status_code == 400

    data = dict(
        file = io.open(f'{os.getcwd()}/test/test_files/Ore.txt', 'rb', buffering=0)
    )
    resp = client.post('/tasks/create-papers', data=data, content_type='multipart/form-data')
    assert resp.status_code == 400

    # Test nonexistent author
    data = dict(
        file = io.open(f'{os.getcwd()}/test/test_files/Ore.txt', 'rb', buffering=0)
    )
    resp = client.post(f'/tasks/create-papers?author_id={author_id + 1}', data=data, content_type='multipart/form-data')
    assert resp.status_code == 404