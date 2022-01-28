from turtle import home
from flask import Flask
app = Flask(__name__)

#Imports application routes
from app import routes
from app import views

app.run(debug=True, host='0.0.0.0', port=5000)