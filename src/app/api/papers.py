from flask import Blueprint, current_app, json, request
from app.api.models import Paper
paper_routes = Blueprint('paper_routes', __name__, template_folder='templates')

# Routes starting with /api/papers