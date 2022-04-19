# Move all imports up a level to be able to access our app
import sys
sys.path.append("..")

from datetime import timedelta
from multiprocessing import Process
import threading

from backend.api.models import Base
from backend.factory import create_app
from backend.task_manager import TaskManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pytest
import os

@pytest.fixture(scope="session")
def database_filepath():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return f"{dir_path}/test_database.db"

@pytest.fixture(scope="session")
def database_url(database_filepath):
    return f"sqlite:///{database_filepath}?check_same_thread=False"

@pytest.fixture(scope="session", autouse=True)
def schema_create(database_filepath, database_url):
    if os.path.exists(database_filepath):
        os.remove(database_filepath)

    engine = create_engine(database_url, echo=False)
    Base.metadata.create_all(engine)

@pytest.fixture(scope="session")
def app(database_url):
    engine = create_engine(database_url, echo=False)
    app = create_app(sessionmaker(bind=engine))
    return app

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def session(app):
    session = app.session_maker()
    yield session
    session.close()

@pytest.fixture(scope="function")
def task_manager(database_url):
    task_manager = TaskManager(
        connection_string = database_url,
        update_check_period = timedelta(milliseconds = 100),
        task_lookup_period = timedelta(milliseconds = 100))
    thread = threading.Thread(target=task_manager.scheduler_loop)

    thread.start()
    yield task_manager
    task_manager.stop()
    thread.join()

# This fixture will be automatically used by each test
@pytest.fixture(scope="function", autouse=True)
def clean_db(app):
    session = app.session_maker()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())

    session.commit()

def pytest_addoption(parser):
    parser.addoption(
        "--scraping", action="store_true", default=False, help="run scraping tests"
    )

def pytest_configure(config):
    config.addinivalue_line("markers", "scraping: mark test as a scraping test")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--scraping"):
        # --scraping given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --scraping option to run")
    for item in items:
        if "scraping" in item.keywords:
            item.add_marker(skip_slow)