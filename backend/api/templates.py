from contextlib import contextmanager
from typing import Callable
from flask import Response, Flask, json
from sqlalchemy.orm import Session

@contextmanager
def db_session(current_app: Flask):
    session = current_app.session_maker()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()