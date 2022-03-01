from factory import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base
import os

db_host = str(os.environ.get('DB_HOST'))
db_user = str(os.environ.get('DB_USER'))
db_pass = str(os.environ.get('DB_PASSWORD'))
db_database = str(os.environ.get('DB_DATABASE'))

connection_string = "mysql://" + db_user + ":" + db_pass  + "@" + db_host + ":3306"  + "/" + db_database

engine = create_engine(connection_string)

Session = sessionmaker(bind=engine)
app = create_app(Session)
Base.metadata.create_all(engine)

app.run(debug=True, host='0.0.0.0', port=5000)