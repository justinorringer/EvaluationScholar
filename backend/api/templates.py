from contextlib import contextmanager
from typing import Callable, Tuple, Optional
from flask import Response, Flask, json
from sqlalchemy.orm import Session

import math

class ApiTemplateError(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code

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

def paginate(query: Callable, parameters: dict) -> Tuple[Callable, Optional[int]]:
    if "limit" in parameters:
        try:
            limit = int(parameters['limit'])
            if limit < 1:
                raise ApiTemplateError("limit must be greater than 0", 400)
        except ValueError:
            raise ApiTemplateError("limit must be an integer", 400)
        
        total_objects = query.count()
        query = query.limit(limit)
        pages = int(math.ceil(total_objects / limit)) if total_objects > 0 else 1

        if "page" in parameters:
            try:
                page = int(parameters['page'])
                if page < 1:
                    raise ApiTemplateError("page must be greater than 0", 400)
                if page > pages:
                    raise ApiTemplateError("paged too far", 404)
            except ValueError:
                raise ApiTemplateError("page must be an integer", 400)
            
            query = query.offset(limit * (page - 1))

        return query, pages
    
    return query, None