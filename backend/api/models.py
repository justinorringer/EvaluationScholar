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

    papers = relationship('Paper', secondary=author_paper, back_populates='authors')
    tags = relationship('Tag', secondary=author_tag, back_populates='authors')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def __init__(self, name):
        self.name = name

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
    #Should we have the title be unique to handle duplicates?
    name = Column(String(100), unique=True, nullable=False)
    #Leave enough characters for 'dd/mm/yyyy', but can just do a year
    year = Column(Integer, unique=False, nullable=False)
    #I believe we were just linking these to the Citation table
    #num_cited=Column(Integer, nullable=False)

    authors = relationship('Author', secondary=author_paper, back_populates='papers')
    citations = relationship('Citation', backref='paper', order_by='Citation.date.desc()')
    jobs = relationship('Job', back_populates='paper')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'latest_citation': None if len(self.citations) == 0 else self.citations[0].to_dict()
        }

    def __init__(self, name, year):
        self.name = name
        self.year = year

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

class JobType(enum.Enum):
    CREATE_PAPER = 1
    UPDATE_CITATIONS = 2
    SCRAPE_AUTHORS = 3

class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_type = Column(Enum(JobType), nullable=False)
    paper_title = Column(String(200), nullable=True)
    paper_id = Column(Integer, ForeignKey('paper.id'), nullable=True)
    priority = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=True)

    paper = relationship('Paper', back_populates='jobs')

    def to_dict(self):
        return {
            'id': self.id,
            'job_type': self.job_type,
            'paper_title': self.paper_title,
            'paper_id': self.paper_id,
            'priority': self.priority,
            'date': self.date,
        }
    
    def __init__(self, job_type, paper_title=None, paper_id=None, priority=0, date=None):
        self.job_type = job_type
        self.paper_title = paper_title
        self.paper_id = paper_id
        self.priority = priority
        self.date = date