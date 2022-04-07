from sqlalchemy import or_, exists, create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
import time
from datetime import datetime, timedelta
from contextlib import contextmanager

from api.models import Task, Paper, Citation, UpdateCitationsTask, Variable
from scraping import scrape_papers


# How often a paper's citation count should be updated
citation_update_period = timedelta(days = 3)

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

class TaskManager():
    def __init__(self, update_check_period: timedelta, task_lookup_period: timedelta, connection_string):
        self.update_check_period = update_check_period
        self.task_lookup_period = task_lookup_period

        engine = create_engine(connection_string, echo=False)
        self.Session = scoped_session(sessionmaker(bind=engine))

        self.enabled = True
        self.running = True

    def disable(self):
        self.enabled = False
    
    def enable(self):
        self.enabled = True

    def stop(self):
        self.running = False

    def scheduler_loop(self):
        last_update_check = datetime.now()
        last_task_check = datetime.now()

        while self.running:
            time.sleep(min(self.update_check_period.total_seconds(), self.task_lookup_period.total_seconds(), 1))

            if not self.enabled:
                continue

            if datetime.now() > last_update_check + self.update_check_period:
                last_update_check = datetime.now()
                self.check_update_tasks()

            if datetime.now() > last_task_check + self.task_lookup_period:
                last_task_check = datetime.now()

                with db_session(self.Session) as session:
                    task = session.query(Task).filter(or_(Task.date == None, Task.date <= datetime.now())).order_by(Task.priority).first()

                    if task is not None:
                        
                        if task.type == "create_paper_task":
                            self.create_paper(session, task.paper_title, task.author)
                        elif task.type == "update_citations_task":
                            self.update_citations(session, task.paper)

                        session.delete(task)

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

    def update_citations(self, session, paper):
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

    def create_paper(self, session, paper_title, author):
        if paper_title == None:
            print("[Task Manager] Paper title is None")
            return

        # Check for an exact match for the given paper title to avoid a scraping call if possible
        existing_paper = session.query(Paper).filter(func.lower(Paper.name) == paper_title.lower()).first()
        if existing_paper is not None:
            existing_paper.authors.append(author)
            print(f"[Task Manager] Added author to existing paper: '{paper_title}'")
            return

        papers = scrape_papers(paper_title)
        if len(papers) == 0:
            print(f"[Task Manager] Failed to scrape paper during creation: '{paper_title}'")
            return
        
        scraped_paper = papers[0]

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
            existing_paper.authors.append(author)
            print(f"[Task Manager] Added author to existing paper: '{paper_title}'")
            return

        paper = Paper(scraped_paper['title'], scraped_paper['year'])
        paper.scholar_id = scraped_paper['id']
        paper.citations.append(Citation(scraped_paper['citations'], datetime.now()))
        paper.authors.append(author)
        session.add(paper)

        print(f"[Task Manager] Created paper: '{paper_title}'")