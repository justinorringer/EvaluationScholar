import random
from flask import Blueprint
routes = Blueprint('routes', __name__, template_folder='templates')

#API routes

@routes.route('/random', methods=['GET'])
def rand():
    return str(random.randint(1, 100))