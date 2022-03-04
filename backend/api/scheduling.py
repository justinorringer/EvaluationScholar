from flask import Blueprint, current_app, json, request

scheduling_routes = Blueprint('scheduling_routes', __name__, template_folder='templates')

# Routes starting with /api/scheduling