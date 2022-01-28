from app import app

from flask import render_template

#Routes for web pages

@app.route('/')
def index():
    return render_template('index.html')