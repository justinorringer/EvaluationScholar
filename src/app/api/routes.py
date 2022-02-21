from flask import Blueprint, current_app, json, request
from app.api.models import Author, Paper
routes = Blueprint('routes', __name__, template_folder='templates')

#API routes

from app.api.authors import author_routes
from app.api.papers import paper_routes
from app.api.tags import tag_routes
from app.api.scrape import scraping_routes

routes.register_blueprint(author_routes)
routes.register_blueprint(paper_routes)
routes.register_blueprint(tag_routes)
routes.register_blueprint(scraping_routes)