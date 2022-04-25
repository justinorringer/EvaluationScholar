from contextlib import contextmanager
import time
from datetime import datetime, timedelta
import threading

import pytest

from backend.api.models import Task, CreatePaperTask, Author, Paper, UpdateCitationsTask
from backend.test import wait_for_task, wait_for_task_count

@pytest.mark.scraping
def test_create_paper(session, task_manager):
    author = Author(name="Test Author", scholar_id="_QnLm3kAAAAJ")
    session.add(author)
    session.flush()

    # Test creating a valid paper

    task = CreatePaperTask("Autonomous Aerial Water Sampling", author.id)
    session.add(task)
    session.commit()

    wait_for_task(task_manager, task.id)

    paper = session.query(Paper).first()
    assert paper.name == "Autonomous aerial water sampling"
    assert paper.year == 2015
    assert len(paper.citations) > 0
    assert paper.citations[0].num_cited > 0
    assert paper.scholar_id == "bhfHsCHhomoJ"
    assert paper.authors[0].name == "Test Author"
    session.commit()

    # Wait for the scrape_author tasks to finish. Only one task should be left: the update citations task
    wait_for_task_count(task_manager, 1)

    # Check for the scraped authors
    scraped_author = session.query(Author).filter(Author.scholar_id == "q7jnx5IAAAAJ").first()
    assert len(scraped_author.papers) == 1
    assert scraped_author.name == "John-Paul Ore"

    scraped_author = session.query(Author).filter(Author.scholar_id == "swPW5FYAAAAJ").first()
    assert len(scraped_author.papers) == 1
    assert scraped_author.name == "Sebastian Elbaum"

    scraped_author = session.query(Author).filter(Author.scholar_id == "mesiHAsAAAAJ").first()
    assert len(scraped_author.papers) == 1
    assert scraped_author.name == "Amy J. Burgin"
    session.commit()

    # Make sure there's enough time for a citation update task to be created
    time.sleep(0.2)

    # Make sure a citation update task was created
    update_task = session.query(UpdateCitationsTask).first()
    assert update_task.paper_id == paper.id
    assert update_task.date > datetime.now() + timedelta(days = 1)

    # Test a paper that doesn't exist in Google Scholar

    task = CreatePaperTask("this paper does not exist like seriously nisuadfhna", author.id)
    session.add(task)

    wait_for_task(task_manager, task.id)

    # Make sure no new papers were added

    assert session.query(Paper).count() == 1
    assert len(session.query(UpdateCitationsTask).all()) == 1

    # Test creating a paper with the same name, different author

    author2 = Author(name="Test Author 2", scholar_id="_QnLm3kAAbAJ")
    session.add(author2)
    session.flush()

    task = CreatePaperTask("Autonomous Aerial Water Sampling", author2.id)
    session.add(task)
    session.commit()

    wait_for_task(task_manager, task.id)

    # Make sure the paper wasn't recreated
    assert session.query(Paper).count() == 1
    assert session.query(UpdateCitationsTask).count() == 1

    # Make sure the author was added to the paper
    assert len(session.query(Paper).first().authors) == 5
    assert len(author2.papers) == 1

    # Try with inexact paper name, will require scraping to match the title with existing paper
    author3 = Author(name="Test Author 3", scholar_id="_QnLm3kAAbAJ")
    session.add(author3)
    session.flush()

    task = CreatePaperTask("Autonomous Aerial Water", author3.id)
    session.add(task)
    session.commit()

    wait_for_task(task_manager, task.id)

    # Make sure the paper wasn't recreated
    assert session.query(Paper).count() == 1

    # Make sure the author was added to the paper
    assert len(session.query(Paper).first().authors) == 6

    # Test a new paper with some same authors
    task = CreatePaperTask("An empirical study on type annotations: Accuracy, speed, and suggestion effectiveness", author.id)
    session.add(task)
    session.commit()

    wait_for_task(task_manager, task.id)

    assert session.query(Paper).count() == 2

    wait_for_task_count(task_manager, 2)

    assert session.query(UpdateCitationsTask).count() == 2
    assert session.query(Author).filter(Author.name == "Carrick Detweiler").first() is not None

    authors = {author.name: author for author in session.query(Author).all()}
    assert len(authors) == 7
    assert "Carrick Detweiler" in authors.keys()
    assert len(authors["John-Paul Ore"].papers) == 2
    assert len(authors["Sebastian Elbaum"].papers) == 2
    assert len(authors["Carrick Detweiler"].papers) == 1
    assert len(authors["Amy J. Burgin"].papers) == 1
    assert len(authors["Test Author"].papers) == 2
    assert len(authors["Test Author 2"].papers) == 1

@pytest.mark.scraping
def test_create_with_scholar_id(session, task_manager):
    author = Author(name="Test Author", scholar_id="_QnLm3kAAAAJ")
    session.add(author)
    session.flush()

    task = CreatePaperTask("lava", author.id, "UK460fxHiUAJ")
    session.add(task)
    session.commit()

    wait_for_task(task_manager, task.id)

    paper = session.query(Paper).first()
    assert paper.name == "Compound and simple lava flows and flood basalts"
    assert paper.scholar_id == "UK460fxHiUAJ"
    assert paper.year == 1971
    assert len(paper.citations) > 0
    assert paper.citations[0].num_cited > 0
    assert len(paper.authors) >= 1

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

    wait_for_task(task_manager, task.id)

    # Make sure the paper's citations were updated
    paper = session.query(Paper).first()
    assert len(paper.citations) > 0
    assert paper.citations[0].num_cited > 0

    # Make sure the task is gone
    assert len(session.query(UpdateCitationsTask).all()) == 1