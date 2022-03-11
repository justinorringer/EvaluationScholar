# Move relative imports up a level to be able to access our app
from cmath import nan
import sys

sys.path.append("..")

from backend.api.models import *
import pytest
from datetime import datetime

def test_citation(session):
    paper = Paper('name', 2000)
    citation = Citation(1, datetime.now())
    paper.citations.append(citation)

    session.add(paper)
    session.commit()

    assert session.query(Citation).count() == 1

    ret_paper = session.query(Paper).all()[0]

    assert len(ret_paper.citations) == 1

    ret_citation = ret_paper.citations[0]

    assert ret_citation.num_cited == 1
    assert ret_citation.paper.id == ret_paper.id

def test_paper(session):
    paper = Paper('name', 2000)
    author = Author('name')

    paper.authors.append(author)

    session.add(paper)
    session.commit()

    assert session.query(Paper).count() == 1

    ret_paper = session.query(Paper).all()[0]

    assert len(ret_paper.authors) == 1
    assert ret_paper.authors[0].id == author.id

    #Check backreference
    assert len(author.papers) == 1
    assert author.papers[0].id == ret_paper.id

    assert ret_paper.name == 'name'
    assert ret_paper.year == 2000

def test_remove(session):
    #Create a paper, and have it be cited
    paper = Paper('name', 2000)
    citation = Citation(100, datetime.now())
    paper.citations.append(citation)

    #Create an author
    author = Author('name')

    paper.authors.append(author)

    #Test for validity
    session.add(paper)
    session.commit()

    assert session.query(Citation).count() == 1

    ret_paper = session.query(Paper).all()[0]

    assert len(ret_paper.citations) == 1

    ret_citation = ret_paper.citations[0]

    assert ret_citation.num_cited == 100
    assert ret_citation.paper.id == ret_paper.id

    assert len(ret_paper.authors) == 1
    assert ret_paper.authors[0].id == author.id

    #Check backreference
    assert len(author.papers) == 1
    assert author.papers[0].id == ret_paper.id

    assert ret_paper.name == 'name'
    assert ret_paper.year == 2000

    session.delete(author)
    session.delete(citation)
    session.delete(paper)
    session.commit()

    assert session.query(Paper).count() == 0

def test_duplicate_paper(session):
    paper1 = nan
    paper2 = nan
    
    try:
        #Create a first paper
        paper1 = Paper('name', 'date')
        session.add(paper1)
        session.commit()

        #Create a paper with the same name (this should be invalid)
        paper2 = Paper('name', 'date2')
        session.add(paper2)
        session.commit()
    except Exception:
        print("Papers can't match")
        session.rollback()
        assert paper1.name == 'name'

def test_issues(session):
    issue = AmbiguousPaperIssue('gid1', 'gid2', 'gid3', 'title1', 'title2', 'title3', 1, 2, 3)
    session.add(issue)
    session.commit()

    assert session.query(AmbiguousPaperIssue).count() == 1

    ret_issue = session.query(AmbiguousPaperIssue).all()[0]

    assert ret_issue.gid_1 == 'gid1'
    assert ret_issue.gid_2 == 'gid2'
    assert ret_issue.title_1 == 'title1'
    assert ret_issue.count_1 == 1
    assert ret_issue.type == 'ambiguous_paper_issue'

    assert session.query(Issue).count() == 1

    ret_generic_issue = session.query(Issue).all()[0]

    assert ret_generic_issue.type == 'ambiguous_paper_issue'

    session.delete(ret_generic_issue)
    session.commit()

    assert session.query(AmbiguousPaperIssue).count() == 0
    assert session.query(Issue).count() == 0