from flask import Blueprint, current_app, json, request
from api.models import Author, Paper
routes = Blueprint('routes', __name__, template_folder='templates')

# File to link all API routes
# Author(s): Tyler Maxwell, Abhinav Kulhari

from api.authors import author_routes
from api.papers import paper_routes
from api.tags import tag_routes
from api.scrape import scraping_routes

routes.register_blueprint(author_routes)
routes.register_blueprint(paper_routes)
routes.register_blueprint(tag_routes)
routes.register_blueprint(scraping_routes)