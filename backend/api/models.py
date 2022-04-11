import enum
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, desc, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# File to handle the creation of different models/tables stored in the MySQL database
# Author(s): Tyler Maxwell, Gage Fringer

Base = declarative_base()

author_paper = Table('author_paper', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('paper_id', Integer, ForeignKey('paper.id'))
)

author_tag = Table('author_tag', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=False, nullable=False)
    scholar_id = Column(String(12), unique=False, nullable=True)

    papers = relationship('Paper', secondary=author_paper, back_populates='authors')
    tags = relationship('Tag', secondary=author_tag, back_populates='authors')

    def get_h_index(self):
        citations = [paper.get_latest_citation().num_cited for paper in 
            filter(lambda p: len(p.citations) > 0, self.papers)]

        paper_counts = [0 for _ in range(len(citations))]
        for citation_count in citations:
            if citation_count > len(citations):
                paper_counts[len(citations) - 1] += 1
            elif citation_count == 0:
                continue
            else:
                paper_counts[citation_count - 1] += 1
        
        cumulative = 0
        for i in reversed(range(len(paper_counts))):
            cumulative += paper_counts[i]
            if cumulative >= i + 1:
                return i + 1
        
        return 0

    def get_i10_index(self):
        return sum(1 for paper in 
            filter(lambda p: len(p.citations) > 0, self.papers)
            if paper.get_latest_citation().num_cited >= 10)

    def to_dict(self, includes = []):
        dict = {
            'id': self.id,
            'name': self.name,
            'scholar_id': self.scholar_id,
        }

        if 'papers' in includes:
            dict['papers'] = [paper.to_dict() for paper in self.papers]
        
        if 'tags' in includes:
            dict['tags'] = [tag.to_dict() for tag in self.tags]

        return dict

    def __init__(self, name, scholar_id):
        self.name = name
        self.scholar_id = scholar_id

class Citation(Base):
    __tablename__ = 'citation'
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('paper.id'), nullable=False)
    num_cited = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'paper_id': self.paper_id,
            'num_cited': self.num_cited,
            'date': self.date,
        }

    def __init__(self, num_cited, date):
        self.num_cited = num_cited
        self.date = date

class Paper(Base):
    __tablename__ = 'paper'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(400), unique=True, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    scholar_id = Column(String(100), unique=False, nullable=True)

    authors = relationship('Author', secondary=author_paper, back_populates='papers')
    citations = relationship('Citation', backref='paper', order_by='Citation.date.desc()', cascade='all, delete-orphan')

    def get_latest_citation(self):
        return None if len(self.citations) == 0 else self.citations[0]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'scholar_id': self.scholar_id,
            'latest_citation': self.get_latest_citation().to_dict() if self.get_latest_citation() else None,
        }

    def __init__(self, name, year, scholar_id = None):
        self.name = name
        self.year = year
        self.scholar_id = scholar_id

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    authors = relationship('Author', secondary=author_tag, back_populates='tags')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __init__(self, name):
        self.name = name

class Task(Base):
    __tablename__ = 'task'

    # Prevent the test SQLite database from reusing deleted IDs
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(80), nullable=False)
    priority = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'task',
        'polymorphic_on':type
    }

class CreatePaperTask(Task):
    __tablename__ = 'create_paper_task'
    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    paper_title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)
    paper_scholar_id = Column(String(40), nullable=True)

    author = relationship('Author')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'priority': self.priority,
            'date': self.date,
            'paper_title': self.paper_title,
            'paper_scholar_id': self.paper_scholar_id,
            'author': self.author.to_dict()
        }

    def __init__(self, paper_title, author_id, paper_scholar_id=None, priority=0, date=None):
        self.paper_title = paper_title
        self.author_id = author_id
        self.paper_scholar_id = paper_scholar_id
        self.priority = priority
        self.date = date

    __mapper_args__ = {
        'polymorphic_identity': 'create_paper_task'
    }

class UpdateCitationsTask(Task):
    __tablename__ = 'update_citations_task'
    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    paper_id = Column(Integer, ForeignKey('paper.id'), nullable=False)

    paper = relationship('Paper', foreign_keys=[paper_id])

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'priority': self.priority,
            'date': self.date,
            'paper': self.paper.to_dict(),
        }

    def __init__(self, paper_id, priority=0, date=None):
        self.paper_id = paper_id
        self.priority = priority
        self.date = date

    __mapper_args__ = {
        'polymorphic_identity': 'update_citations_task'
    }

class ScrapeAuthorTask(Task):
    __tablename__ = 'scrape_author_task'
    id = Column(Integer, ForeignKey('task.id'), primary_key=True)
    author_id = Column(Integer, ForeignKey('author.id'), nullable=False)

    author = relationship('Author')

    def __init__(self, author_id, priority=0, date=None):
        self.author_id = author_id
        self.priority = priority
        self.date = date

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'priority': self.priority,
            'date': self.date,
            'author': self.author.to_dict(),
        }
    
    __mapper_args__ = {
        'polymorphic_identity': 'scrape_author_task'
    }

class Issue(Base):
    __tablename__ = "issue"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(80), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'issue',
        'polymorphic_on':type
    }

class AmbiguousPaperIssue(Issue):
    __tablename__ = "ambiguous_paper_issue"
    id = Column(Integer, ForeignKey('issue.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'ambiguous_paper_issue',
    }

    author_name = Column(String(80), nullable=False)
    paper_id_1 = Column(Integer, ForeignKey('paper.id'), nullable=False)
    paper_id_2 = Column(Integer, ForeignKey('paper.id'), nullable=False)
    paper_id_3 = Column(Integer, ForeignKey('paper.id'), nullable=True)

    paper_1 = relationship('Paper', foreign_keys=[paper_id_1])
    paper_2 = relationship('Paper', foreign_keys=[paper_id_2])
    paper_3 = relationship('Paper', foreign_keys=[paper_id_3])

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'author_name': self.author_name,
            'paper_1': self.paper_1.to_dict(),
            'paper_2': self.paper_2.to_dict(),
            'paper_3': None if self.paper_3 is None else self.paper_3.to_dict(),
        }
    
    def __init__(self, author_name, paper_id_1, paper_id_2, paper_id_3 = None):
        self.author_name = author_name
        self.paper_id_1 = paper_id_1
        self.paper_id_2 = paper_id_2
        self.paper_id_3 = paper_id_3

class Variable(Base):
    __tablename__ = "variable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)
    value = Column(String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
        }
    
    def __init__(self, name, value):
        self.name = name
        self.value = value