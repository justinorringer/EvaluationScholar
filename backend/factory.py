from flask import Flask
import os

def create_app(session_maker):
    app = Flask(__name__)

    from api.routes import routes
    from views import views
    
    app.register_blueprint(routes)
    app.register_blueprint(views)

    app.session_maker = session_maker

    return app

def create_connection_string():
    db_host = str(os.environ.get('DB_HOST'))
    db_user = str(os.environ.get('DB_USER'))
    db_pass = str(os.environ.get('DB_PASSWORD'))
    db_database = str(os.environ.get('DB_DATABASE'))

    return f"mysql://{db_user}:{db_pass}@{db_host}:3306/{db_database}"