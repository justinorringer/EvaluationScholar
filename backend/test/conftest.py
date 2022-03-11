# Move all imports up a level to be able to access our app
import sys
sys.path.append("..")

from backend.api.models import Base
from backend.factory import create_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

@pytest.fixture(scope="session")
def app():
    engine=create_engine('sqlite://',echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    app = create_app(Session)
    return app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    return app.session_maker()

# This fixture will be automatically used by each test
@pytest.fixture(autouse=True)
def clean_db(session):
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()

def pytest_addoption(parser):
    parser.addoption(
        "--scraping", action="store_true", default=False, help="run scraping tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as a scraping test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--scraping"):
        # --scraping given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --scraping option to run")
    for item in items:
        if "scraping" in item.keywords:
            item.add_marker(skip_slow)