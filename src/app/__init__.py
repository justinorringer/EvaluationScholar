from app.factory import create_app
from app.database import Session

test = 3 

def start_app():
    app = create_app(Session())

    app.run(debug=True, host='0.0.0.0', port=5000)