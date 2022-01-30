# Move all imports up a level to be able to access our app
from email.mime import audio
import sys
sys.path.append("..")

from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import os

# Create the SQLAlchemy session to be used by the tests
@pytest.fixture(scope="session")
def session():
    # Create an SQLite database in memory
    engine=create_engine('sqlite://',echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# This fixture will be automatically used by each test
@pytest.fixture(autouse=True)
def clean_db(session):
    Base.metadata.drop_all(session.bind)
    Base.metadata.create_all(session.bind)