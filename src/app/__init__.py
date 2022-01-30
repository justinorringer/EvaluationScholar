from app.factory import create_app

test = 3 

def start_app():
    app = create_app()

    app.run(debug=True, host='0.0.0.0', port=5000)