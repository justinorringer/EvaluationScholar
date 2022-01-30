import os
from app.factory import create_app

def start_app():
    app = create_app()

    db_host = str(os.environ.get('DB_HOST'))
    db_user = str(os.environ.get('DB_USER'))
    db_pass = str(os.environ.get('DB_PASSWORD'))
    db_database = str(os.environ.get('DB_DATABASE'))

    connection = db_host + "://" + db_user + ":" + db_pass  + "@mysql-database:3306" + "/" + db_database

    app.config['SQLALCHEMY_DATABASE_URI'] = connection

    app.run(debug=True, host='0.0.0.0', port=5000)