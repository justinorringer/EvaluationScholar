from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.models import db
    db.init_app(app)

    from app.routes import routes
    from app.views import views
    
    app.register_blueprint(routes)
    app.register_blueprint(views)

    return app