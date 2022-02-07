# Move relative imports up a level to be able to access our app
import sys
sys.path.append("..")

from app.api.models import *
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
    author = Author('name', 'institution')

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