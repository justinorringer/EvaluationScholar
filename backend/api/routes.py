from flask import Blueprint, current_app, json, request
from api.models import Author, Paper, User
from api.templates import db_session
routes = Blueprint('routes', __name__, template_folder='templates')

# File to link all API routes
# Author(s): Tyler Maxwell, Abhinav Kulhari

@routes.before_request
def before_request():
    if not current_app.disable_auth:
        with db_session(current_app) as session:
            shib_uid = request.headers.get('X-SHIB_UID')

            if shib_uid is None:
                return json.dumps({'error': 'No Shibboleth UID'}), 401
            
            user = session.query(User).filter(User.shib_uid == shib_uid).first()

            if user is None:
                return json.dumps({'error': 'User not authorized'}), 401

from api.authors import author_routes
from api.papers import paper_routes
from api.tags import tag_routes
from api.scrape import scraping_routes
from api.issues import issue_routes
from api.tasks import task_routes
from api.task_manager import task_manager_routes

routes.register_blueprint(author_routes)
routes.register_blueprint(paper_routes)
routes.register_blueprint(tag_routes)
routes.register_blueprint(scraping_routes)
routes.register_blueprint(issue_routes)
routes.register_blueprint(task_routes)
routes.register_blueprint(task_manager_routes)