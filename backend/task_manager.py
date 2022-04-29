from sqlalchemy import or_, exists, create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
import time
from datetime import datetime, timedelta
from contextlib import contextmanager

from api.models import Task, UpdateCitationsTask, ScrapeAuthorTask
from api.models import Paper, Citation, Author, Variable
from api.models import Issue, AmbiguousPaperIssue, AmbiguousPaperChoice
from scraping import scrape_papers
from scraping.google_scholar import get_profile_page_html, parse_profile_page_name
from multiprocessing import Process
from threading import Thread
from threading import Lock

# Use the lock to prevent multiple threads from accessing the database at the same time
# This prevents duplicate data being created (as a result of multiple threads trying to create the same data and both checking for the duplicate before either commit)
lock = Lock()

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
    session.commit()

def update_citations(session, paper):
    if paper is None:
        print("[Task Manager] Paper is None")
        return

    scraped_papers = scrape_papers(paper.name)
    if len(scraped_papers) == 0:
        print(f"[Task Manager] Failed to scrape paper for citation update: '{paper.name}'")
        return

    # TODO: Match using scholar id
    scraped_paper = scraped_papers[0]
    if scraped_paper['citations'] is None:
        print(f"[Task Manager] Failed to scrape citations for paper in citation update: '{paper.name}'")
        return
    
    paper.citations.append(Citation(scraped_paper['citations'], datetime.now()))

    print(f"[Task Manager] Updated citations for paper: '{paper.name}'")
    session.commit()

def create_and_link_authors(session, paper, scraped_authors):
    with lock:
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

def create_ambiguous_issue(session, author, query, scraped_papers):
    with lock:
        issue = AmbiguousPaperIssue(author.id, query)
        session.add(issue)
        session.flush()

        choices = [AmbiguousPaperChoice(
            name = p['title'],
            year = p['year'],
            scholar_id = p['id'],
            citations = p['citations'],
            issue_id = issue.id,
            author_names_list = [a['name'] for a in p['authors']]
        ) for p in scraped_papers]

        session.add_all(choices)
        session.commit()

        print(f"[Task Manager] Created ambiguous paper issue for: '{query}'")

def create_paper(session, paper_title, author, paper_scholar_id):
    if paper_title == None:
        print("[Task Manager] Paper title is None")
        return

    scraped_papers = scrape_papers(paper_title)
    if len(scraped_papers) == 0:
        print(f"[Task Manager] Failed to scrape paper during creation: '{paper_title}'")
        return
    
    # Choose the correct scraped paper to use, or create an ambiguous issue if that's not possible
    if paper_scholar_id is not None:
        # Pick the one with the correct scholar id if it's given
        scraped_paper = next(iter(p for p in scraped_papers if p['id'] == paper_scholar_id), None)

        if scraped_paper is None:
            print(f"[Task Manager] Failed to find scraped paper with id: '{paper_scholar_id}' and title: '{paper_title}'")
            return
    elif len(scraped_papers) == 1:
        # If there's only one result, use it
        scraped_paper = scraped_papers[0]
    else:
        # Otherwise, we can't pick the correct paper, so create an ambiguous issue
        create_ambiguous_issue(session, author, paper_title, scraped_papers)
        return
        
    with lock:
        existing_paper = session.query(Paper).filter(Paper.scholar_id == scraped_paper['id']).first()
        if existing_paper is not None:
            if existing_paper in author.papers:
                print(f"[Task Manager] Paper '{paper_title}' already exists for author '{author.name}'")
                return

            existing_paper.authors.append(author)
            session.commit()
            print(f"[Task Manager] Added author {author.name} to existing paper: '{existing_paper.name}'")
            return

        paper = Paper(scraped_paper['title'], scraped_paper['year'], scraped_paper['id'])

        paper.citations.append(Citation(scraped_paper['citations'], datetime.now()))
        paper.authors.append(author)

        session.add(paper)
        session.commit()

    print(f"[Task Manager] Created paper: '{paper_title}'")

    # This feature creates a large number of authors, most of which are irrelevant data.
    # Parts of our frontend don't perform well with a large number of authors, so for now we're leaving it disabled.
    #create_and_link_authors(session, paper, scraped_paper['authors'])

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

    session.close()
    Session.close()
    engine.dispose()

class TaskManager():
    def __init__(self,
    connection_string: str,
    update_check_period: timedelta = timedelta(seconds=5),
    task_lookup_period: timedelta = timedelta(seconds=5),
    max_concurrent_tasks: int = 3):
        self.update_check_period = update_check_period
        self.task_lookup_period = task_lookup_period
        self.connection_string = connection_string
        self.max_concurrent_tasks = max_concurrent_tasks

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
            
            self.running_tasks = [task for task in self.running_tasks if task['thread'].is_alive()]

            if not self.enabled:
                continue

            if datetime.now() > last_update_check + self.update_check_period:
                last_update_check = datetime.now()
                self.check_update_tasks()

            if len(self.running_tasks) < self.max_concurrent_tasks and datetime.now() > last_task_check + self.task_lookup_period:
                session = self.Session()
                space_available = self.max_concurrent_tasks - len(self.running_tasks)

                tasks = session.query(Task)
                tasks = tasks.filter(or_(Task.date == None, Task.date <= datetime.now()))
                tasks = tasks.order_by(Task.priority)
                tasks = tasks.limit(space_available).all()

                for task in tasks:
                    task_id = task.id

                    session.delete(task)
                    session.commit()

                    task_thread = Thread(target=handle_task, args=(self.connection_string, task))
                    task_thread.start()

                    # Keep track of task id so tests can check if task is done
                    self.running_tasks.append({
                        'thread': task_thread,
                        'task_id': task_id
                    })
                
                session.close()
                last_task_check = datetime.now()

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