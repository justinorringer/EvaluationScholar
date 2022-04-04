from sqlalchemy import or_, exists
from sqlalchemy.orm import scoped_session
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
    def __init__(self, update_check_period: timedelta, task_lookup_period: timedelta, Session):
        self.update_check_period = update_check_period
        self.task_lookup_period = task_lookup_period
        self.Session = scoped_session(Session)

    def scheduler_loop(self):
        last_update_check = datetime.now()
        last_task_check = datetime.now()

        while True:
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

            time.sleep(1)

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

        papers = scrape_papers(paper.name)
        if len(papers) == 0:
            print(f"[Task Manager] Failed to scrape paper for citation update: '{paper.name}'")
            return

        paper = papers[0]
        if paper.citations is None:
            print(f"[Task Manager] Failed to scrape citations for paper in citation update: '{paper.name}'")
            return
        
        paper.citations.append(Citation(paper.citations, datetime.now()))

        print(f"[Task Manager] Updated citations for paper: '{paper.name}'")

    def create_paper(self, session, paper_title, author):
        if paper_title == None:
            print("[Task Manager] Paper title is None")
            return

        if session.query(Paper).filter(Paper.name == paper_title).first() is not None:
            print(f"[Task Manager] Paper already exists: '{paper_title}'")
            return

        papers = scrape_papers(paper_title)
        if len(papers) == 0:
            print(f"[Task Manager] Failed to scrape paper during creation: '{paper_title}'")
            return
        
        scraped_paper = papers[0]

        if scraped_paper.citations is None:
            print(f"[Task Manager] Failed to scrape paper citations during creation: '{paper_title}'")
            return
        
        if scraped_paper.year is None:
            print(f"[Task Manager] Failed to scrape paper year during creation: '{paper_title}'")
            return

        paper = Paper(paper_title, scraped_paper.year)
        paper.citations.append(Citation(scraped_paper.year, datetime.now()))
        paper.authors.append(author)
        session.add(paper)

        print(f"[Task Manager] Created paper: '{paper_title}'")