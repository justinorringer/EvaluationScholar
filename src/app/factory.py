from flask import Flask

def create_app(session):
    app = Flask(__name__)

    from app.api.routes import routes
    from app.views import views
    
    app.register_blueprint(routes)
    app.register_blueprint(views)

    app.session = session

    return app