# Move all imports up a level to be able to access our app
import sys
sys.path.append("..")

from app.api.models import Base
from app.factory import create_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

@pytest.fixture(scope="session")
def app():
    engine=create_engine('sqlite://',echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    app = create_app(Session())
    return app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    return app.session

# This fixture will be automatically used by each test
@pytest.fixture(autouse=True)
def clean_db(app, session):
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()