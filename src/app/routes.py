import random
from flask import Blueprint, current_app
from app.models import Author
routes = Blueprint('routes', __name__, template_folder='templates')

#API routes

@routes.route('/random', methods=['GET'])
def rand():
    return str(random.randint(1, 100))

@routes.route('/createauthor', methods=['GET'])
def createpaper():
    author = Author('name', 'institution')
    current_app.session.add(author)
    current_app.session.commit()
    return str(author.id)