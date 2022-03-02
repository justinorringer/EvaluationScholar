from factory import create_app, create_connection_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base

import os
import threading

engine = create_engine(create_connection_string())

Session = sessionmaker(bind=engine)
session = Session()
app = create_app(session)
Base.metadata.create_all(engine)

from scheduler import scheduler_loop
threading.Thread(target=scheduler_loop).start()

app.run(debug=True, host='0.0.0.0', port=5000)