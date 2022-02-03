#Defines data Bases for the application
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

author_paper = Table('author_paper', Base.metadata,
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('paper_id', Integer, ForeignKey('paper.id'))
)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=False, nullable=False)

    #Won't allow null, but can keep the most recent institution, regardless of if they're still teaching
    institution=Column(String(80), unique=False, nullable=False)

    papers = relationship('Paper', secondary=author_paper, back_populates='authors')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'institution': self.institution,
        }

    def __init__(self, name, institution):
        self.name = name
        self.institution = institution

class Paper(Base):
    __tablename__ = 'paper'
    id = Column(Integer, primary_key=True, autoincrement=True)
    #Should we have the title be unique to handle duplicates?
    name = Column(String(100), unique=True, nullable=False)
    #Leave enough characters for 'dd/mm/yyyy', but can just do a year
    date = Column(String(10), unique=False, nullable=False)
    #I believe we were just linking these to the Citation table
    #num_cited=Column(Integer, nullable=False)

    authors = relationship('Author', secondary=author_paper, back_populates='papers')
    citations = relationship('Citation', backref='paper')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
        }

    def __init__(self, name, date):
        self.name = name
        self.date = date

class Citation(Base):
    __tablename__ = 'citation'
    id = Column(Integer, primary_key=True)
    paper_id = Column(Integer, ForeignKey('paper.id'), nullable=False)
    num_cited = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'paper_id': self.paper_id,
            'num_cited': self.num_cited,
        }

    def __init__(self, num_cited):
        self.num_cited = num_cited