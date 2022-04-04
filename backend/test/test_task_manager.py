from contextlib import contextmanager
import time
from datetime import datetime, timedelta
import threading

import pytest

from backend.api.models import Task, CreatePaperTask, Author, Paper, UpdateCitationsTask

def wait_for_task(session, id):
    start_time = datetime.now()
    while True:
        print(session.query(Task).filter(Task.id == id).first())
        if session.query(Task).filter(Task.id == id).first() is None:
            return
            
        time.sleep(1)

        if datetime.now() > start_time + timedelta(seconds = 30):
            pytest.fail("CreatePaperTask not resolved")
        
        session.commit()

@pytest.mark.scraping
def test_create_paper(session, task_manager):
    author = Author(name="Test Author", scholar_id="_QnLm3kAAAAJ")
    session.add(author)
    session.flush()

    # Test creating a valid paper

    task = CreatePaperTask("Autonomous Aerial Water Sampling", author.id)
    session.add(task)
    session.commit()

    wait_for_task(session, task.id)

    paper = session.query(Paper).first()
    assert paper.name == "Autonomous Aerial Water Sampling"
    assert paper.year == 2015
    assert len(paper.citations) > 0
    assert paper.citations[0].num_cited > 0
    assert paper.scholar_id == "bhfHsCHhomoJ"
    assert paper.authors[0].name == "Test Author"

    # Make sure there's enough time for a citation update task to be created
    time.sleep(0.2)

    # Make sure this session's data is updated
    session.expunge_all()

    # Make sure a citation update task was created
    update_task = session.query(UpdateCitationsTask).first()
    assert update_task.paper_id == paper.id
    assert update_task.date > datetime.now() + timedelta(days = 1)

    # Test a paper that doesn't exist in Google Scholar

    task = CreatePaperTask("this paper does not exist like seriously nisuadfhna", author.id)
    session.add(task)

    wait_for_task(session, task.id)

    # Make sure no new papers were added

    assert len(session.query(Paper).all()) == 1
    assert len(session.query(UpdateCitationsTask).all()) == 1

@pytest.mark.scraping
def test_update_citations(session, task_manager):
    author = Author(name="Test Author", scholar_id="_QnLm3kAAAAJ")
    session.add(author)
    session.flush()

    paper = Paper(name="Autonomous Aerial Water Sampling", year=2015)
    paper.scholar_id = "bhfHsCHhomoJ"
    paper.authors.append(author)
    session.add(paper)
    session.commit()

    time.sleep(0.2)

    # Make sure a citation update task was created
    update_task = session.query(UpdateCitationsTask).first()
    assert update_task.paper_id == paper.id
    assert update_task.date > datetime.now() + timedelta(days = 1)

    # Create an instant update task
    task = UpdateCitationsTask(paper.id)
    session.add(task)
    session.commit()

    wait_for_task(session, task.id)

    # Make sure the paper's citations were updated
    paper = session.query(Paper).first()
    assert len(paper.citations) > 0
    assert paper.citations[0].num_cited > 0

    # Make sure the task is gone
    assert len(session.query(UpdateCitationsTask).all()) == 1