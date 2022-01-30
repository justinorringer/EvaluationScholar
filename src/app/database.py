from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os

db_host = str(os.environ.get('DB_HOST'))
db_user = str(os.environ.get('DB_USER'))
db_pass = str(os.environ.get('DB_PASSWORD'))
db_database = str(os.environ.get('DB_DATABASE'))

connection_string = db_host + "://" + db_user + ":" + db_pass  + "@mysql-database:3306" + "/" + db_database

engine = create_engine(connection_string)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()