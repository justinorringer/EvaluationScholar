#Defines data models for the application
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

author_paper = db.Table('author_paper', db.Model.metadata,
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'))
)

class Author(db.Model):
    __tablename__ = 'author'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(80), unique=False, nullable=False)

    #Won't allow null, but can keep the most recent institution, regardless of if they're still teaching
    institution=db.Column(db.String(80), unique=False, nullable=False)

    papers = db.relationship('Paper', secondary=author_paper, back_populates='authors')

    def __init__(self, name, institution):
        self.name = name
        self.institution = institution

class Paper(db.Model):
    __tablename__ = 'paper'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    #Should we have the title be unique to handle duplicates?
    name=db.Column(db.String(100), unique=True, nullable=False)
    #Leave enough characters for 'dd/mm/yyyy', but can just do a year
    date=db.Column(db.String(10), unique=False, nullable=False)
    #I believe we were just linking these to the Citation table
    #num_cited=db.Column(db.Integer, nullable=False)
    auth_name=db.Column(db.String(40), nullable=False)

    authors = db.relationship('Author', secondary=author_paper, back_populates='papers')

    def __init__(self, name, date, auth_name):
        self.name = name
        self.date = date
        self.auth_name = auth_name

class Citation(db.Model):
    __tablename__ = 'citation'
    id=db.Column(db.Integer, primary_key=True)
    id_cited_paper=db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False)
    num_cited=db.Column(db.Integer, nullable=False)

    def __init__(self, id_cited_paper, num_cited):
        self.id_cited_paper = id_cited_paper
        self.num_cited = num_cited