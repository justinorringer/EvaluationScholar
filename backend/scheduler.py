from factory import create_connection_string
from sqlalchemy import create_engine, desc, text, or_, not_
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime, timedelta

from api.models import Job, Paper, Citation, JobType
from scraping import scrape_paper, scrape_citations

engine = create_engine(create_connection_string())

Session = sessionmaker(bind=engine)

# How often to look for a new job
job_lookup_period = timedelta(seconds = 10)

# How often to check for papers that are missing a citation update job
update_check_period = timedelta(seconds = 10)

# How often a paper's citation count should be updated
citation_update_period = timedelta(days = 3)

def create_paper(session, paper_title):
    if paper_title == None:
        print("[Scheduler] Paper title is None")
        return

    if session.query(Paper).filter(Paper.name == paper_title).first() is not None:
        print(f"[Scheduler] Paper already exists: '{paper_title}'")
        return

    citations, year = scrape_paper(paper_title)
    if citations is None or year is None:
        print(f"[Scheduler] Failed to scrape paper: '{paper_title}'")
        return
    
    paper = Paper(paper_title, year)
    paper.citations.append(Citation(citations, datetime.now()))
    session.add(paper)

    print(f"[Scheduler] Created paper: '{paper_title}'")

def update_citations(session, paper):
    if paper is None:
        print("[Scheduler] Paper is None")
        return

    citations = scrape_citations(paper.name)
    if citations is None:
        print(f"[Scheduler] Failed to scrape citations for paper: '{paper.name}'")
        return
    
    paper.citations.append(Citation(citations, datetime.now()))

    print(f"[Scheduler] Updated citations for paper: '{paper.name}'")

def scrape_authors(paper):
    print(f"[Scheduler] Author scraping not implemented yet: '{paper.name}'")

def create_citation_update_job(session, paper):
    update_job = Job(JobType.UPDATE_CITATIONS, paper.name, paper.id, priority=0, date=datetime.now() + citation_update_period)
    session.add(update_job)

    print(f"[Scheduler] Created citation update job for paper: '{paper.name}' at {update_job.date}")

def check_update_jobs(session):
    papers = session.query(Paper).filter(not_(Paper.jobs.any(Job.job_type == JobType.UPDATE_CITATIONS))).all()
    for paper in papers:
        create_citation_update_job(session, paper)

def scheduler_loop():
    last_update_check = datetime.now()
    last_job_check = datetime.now()

    while True:
        if datetime.now() > last_update_check + update_check_period:
            with Session() as session:
                with session.begin():
                    last_update_check = datetime.now()
                    check_update_jobs(session)

        if datetime.now() > last_job_check + job_lookup_period:
            last_job_check = datetime.now()

            with Session() as session:
                with session.begin():
                    job = session.query(Job).filter(or_(Job.date == None, Job.date <= datetime.now())).order_by(Job.priority).first()

                    if job is not None:
                        if job.job_type == JobType.CREATE_PAPER:
                            create_paper(session, job.paper_title)
                        elif job.job_type == JobType.UPDATE_CITATIONS:
                            update_citations(session, job.paper)
                            create_citation_update_job(session, job.paper)

                        session.delete(job)

        time.sleep(1)

        