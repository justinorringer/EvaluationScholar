from flask import render_template, Blueprint
views = Blueprint('views', __name__, template_folder='templates')

#Routes for web pages

@views.route('/')
def index():
    return render_template('index.html')