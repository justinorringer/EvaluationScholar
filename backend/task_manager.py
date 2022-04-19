from sqlalchemy import or_, exists, create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
import time
from datetime import datetime, timedelta
from contextlib import contextmanager

from api.models import Task, Paper, Citation, UpdateCitationsTask, Variable, Author, ScrapeAuthorTask
from scraping import scrape_papers
from scraping.google_scholar import get_profile_page_html, parse_profile_page_name
from multiprocessing import Process

@contextmanager
def db_session(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"[Task Manager] Error: {e}")
    finally:
        session.close()

def scrape_author(session, author):
    html = get_profile_page_html(author.scholar_id)
    if html is None:
        print(f"[Task Manager] Failed to scrape author: '{author.name}'")
        return
    
    name = parse_profile_page_name(html)
    if name is None:
        print(f"[Task Manager] Failed to parse name for author: '{author.name}'")
        return
    
    author.name = name
    print(f"[Task Manager] Scraped author details: '{author.name}'")

def update_citations(session, paper):
    if paper is None:
        print("[Task Manager] Paper is None")
        return

    scraped_papers = scrape_papers(paper.name)
    if len(scraped_papers) == 0:
        print(f"[Task Manager] Failed to scrape paper for citation update: '{paper.name}'")
        return

    scraped_paper = scraped_papers[0]
    if scraped_paper['citations'] is None:
        print(f"[Task Manager] Failed to scrape citations for paper in citation update: '{paper.name}'")
        return
    
    paper.citations.append(Citation(scraped_paper['citations'], datetime.now()))

    print(f"[Task Manager] Updated citations for paper: '{paper.name}'")

def create_and_link_authors(session, paper, scraped_authors):
    for scraped_author in scraped_authors:
        existing_author = session.query(Author).filter(Author.scholar_id == scraped_author['id']).first()
        if existing_author is None:
            author = Author(scraped_author['name'], scraped_author['id'])
            session.add(author)
            author.papers.append(paper)
            session.flush()

            scrape_author_task = ScrapeAuthorTask(author.id)
            session.add(scrape_author_task)
            print(f"[Task Manager] Created new scraped author: '{author.name}' and linked to paper: '{paper.name}'")
        else:
            existing_author.papers.append(paper)
            print(f"[Task Manager] Linked scraped author: '{existing_author.name}' to paper: '{paper.name}'")
    
    session.commit()

def create_paper(session, paper_title, author, paper_scholar_id):
    if paper_title == None:
        print("[Task Manager] Paper title is None")
        return

    # Check for an exact match for the given paper title to avoid a scraping call if possible
    existing_paper = session.query(Paper).filter(func.lower(Paper.name) == paper_title.lower()).first()
    if existing_paper is not None:
        if existing_paper in author.papers:
            print(f"[Task Manager] Paper '{paper_title}' already exists for author '{author.name}'")
            return

        existing_paper.authors.append(author)
        print(f"[Task Manager] Added author to existing paper: '{paper_title}'")
        return

    scraped_papers = scrape_papers(paper_title)
    if len(scraped_papers) == 0:
        print(f"[Task Manager] Failed to scrape paper during creation: '{paper_title}'")
        return
    
    # Select the correct scraped paper to use
    # If a scholar id is given, use that paper
    # Otherwise, use the first paper
    # TODO: Raise an ambiguous paper issue depending on the results
    if paper_scholar_id is not None:
        scraped_paper = next(filter(lambda p: p['id'] == paper_scholar_id, scraped_papers), None)
        if scraped_paper is None:
            print(f"[Task Manager] Failed to find scraped paper with id: '{paper_scholar_id}' and title: '{paper_title}'")
            return
    else:
        scraped_paper = scraped_papers[0]

    if scraped_paper['citations'] is None:
        print(f"[Task Manager] Failed to scrape paper citations during creation: '{paper_title}'")
        return
    
    if scraped_paper['year'] is None:
        print(f"[Task Manager] Failed to scrape paper year during creation: '{paper_title}'")
        return
    
    if scraped_paper['id'] is None:
        print(f"[Task Manager] Failed to scrape paper scholar id during creation: '{paper_title}'")
        return
    
    if scraped_paper['title'] is None:
        print(f"[Task Manager] Failed to scrape paper title during creation: '{paper_title}'")
        return
    
    existing_paper = session.query(Paper).filter(Paper.name == scraped_paper['title']).first()
    if existing_paper is not None:
        if existing_paper in author.papers:
            print(f"[Task Manager] Paper '{paper_title}' already exists for author '{author.name}'")
            return

        existing_paper.authors.append(author)
        print(f"[Task Manager] Added author to existing paper: '{existing_paper.name}'")
        return

    paper = Paper(scraped_paper['title'], scraped_paper['year'], scraped_paper['id'])

    paper.citations.append(Citation(scraped_paper['citations'], datetime.now()))
    paper.authors.append(author)

    session.add(paper)

    print(f"[Task Manager] Created paper: '{paper_title}'")

    create_and_link_authors(session, paper, scraped_paper['authors'])

def handle_task(connection_string, task):
    engine = create_engine(connection_string, echo=False)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()

    if task.type == "create_paper_task":
        author = session.query(Author).filter(Author.id == task.author_id).first()
        create_paper(session, task.paper_title, author, task.paper_scholar_id)
    elif task.type == "update_citations_task":
        paper = session.query(Paper).filter(Paper.id == task.paper_id).first()
        update_citations(session, paper)
    elif task.type == "scrape_author_task":
        author = session.query(Author).filter(Author.id == task.author_id).first()
        scrape_author(session, author)

    session.commit()
    session.close()
    Session.close()
    engine.dispose()

class TaskManager():
    def __init__(self,
    connection_string: str,
    update_check_period: timedelta = timedelta(seconds=5),
    task_lookup_period: timedelta = timedelta(seconds=5),
    task_timeout: timedelta = timedelta(minutes=2),
    max_concurrent_tasks: int = 3):
        self.update_check_period = update_check_period
        self.task_lookup_period = task_lookup_period
        self.connection_string = connection_string
        self.max_concurrent_tasks = max_concurrent_tasks
        self.task_timeout = task_timeout

        engine = create_engine(connection_string, echo=False)
        self.Session = scoped_session(sessionmaker(bind=engine))

        self.enabled = True
        self.running = True

        self.running_tasks = []

    def disable(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True

    def stop(self):
        self.running = False

    def get_task_done(self, task_id: int):
        session = self.Session()

        if session.query(Task).filter(Task.id == task_id).first() is not None:
            session.close()
            return False

        session.close()

        return not any(task_id == task['task_id'] for task in self.running_tasks)
    
    def get_total_task_count(self):
        session = self.Session()

        count = session.query(Task).count()

        session.close()

        return count + len(self.running_tasks)

    def scheduler_loop(self):
        last_update_check = datetime.now()
        last_task_check = datetime.now()

        while self.running:
            time.sleep(min(self.update_check_period.total_seconds(), self.task_lookup_period.total_seconds(), 1))

            # Remove any finished task processes or processes that have timed out
            for task in self.running_tasks:
                task['process'].join(timeout=0)
            
            self.running_tasks = [task for task in self.running_tasks if task['process'].is_alive() and datetime.now() - task['start_time'] < self.task_timeout]

            if not self.enabled:
                continue

            if datetime.now() > last_update_check + self.update_check_period:
                last_update_check = datetime.now()
                self.check_update_tasks()

            if len(self.running_tasks) < self.max_concurrent_tasks and datetime.now() > last_task_check + self.task_lookup_period:
                session = self.Session()
                task = session.query(Task).filter(or_(Task.date == None, Task.date <= datetime.now())).order_by(Task.priority).first()
            
                if task is not None:
                    task_id = task.id

                    session.delete(task)
                    session.commit()
                    session.close()

                    task_process = Process(target=handle_task, args=(self.connection_string, task))
                    task_process.start()

                    # Need to keep track of start time to timeout
                    # Keep track of task id so tests can check if task is done
                    self.running_tasks.append({
                        'process': task_process,
                        'start_time': datetime.now(),
                        'task_id': task_id
                    })
                else:
                    # Only wait if there aren't any tasks to run
                    last_task_check = datetime.now()
                    session.close()

    def check_update_tasks(self):
        with db_session(self.Session) as session:
            citaion_update_period = session.query(Variable).filter(Variable.name == "citation_update_period").first()

            if citaion_update_period is None:
                citaion_update_period = "3"
                session.add(Variable("citation_update_period", citaion_update_period))
            else:
                citaion_update_period = citaion_update_period.value

            update_delta = timedelta(days = int(citaion_update_period))
            papers = session.query(Paper).filter(~exists().where(Paper.id == UpdateCitationsTask.paper_id))
            for paper in papers:
                session.add(UpdateCitationsTask(paper.id, 0, datetime.now() + update_delta))