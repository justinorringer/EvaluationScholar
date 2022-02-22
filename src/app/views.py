from flask import render_template, Blueprint, jsonify
from flask_cors import CORS, cross_origin
views = Blueprint('views', __name__, template_folder='templates')

#Routes for web pages

@views.route('/')
@cross_origin()
def index():
    return jsonify(render_template('index.html'))

@views.route('/api/docs')
def docs():
    return render_template('swaggerui.html')

