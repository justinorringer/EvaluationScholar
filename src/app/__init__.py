from flask import Flask
import os
app = Flask(__name__)

db_host = str(os.environ.get('DB_HOST'))
db_user = str(os.environ.get('DB_USER'))
db_pass = str(os.environ.get('DB_PASSWORD'))
db_database = str(os.environ.get('DB_DATABASE'))

connection = db_host + "://" + db_user + ":" + db_pass  + "@mysql-database:3306" + "/" + db_database
print(connection)

app.config['SQLALCHEMY_DATABASE_URI'] = connection

#Imports application routes
from app import routes
from app import views

from app.models import db, Author
db.init_app(app)
db.create_all()

app.run(debug=True, host='0.0.0.0', port=5000)