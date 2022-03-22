from factory import create_app, create_connection_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from api.models import Base
from datetime import timedelta

import threading

engine = create_engine(create_connection_string(), echo=False)

Session = sessionmaker(bind=engine)
app = create_app(scoped_session(Session))
Base.metadata.create_all(engine)

from task_manager import TaskManager
task_manager = TaskManager(timedelta(seconds = 1), timedelta(seconds = 1), Session)
threading.Thread(target=task_manager.scheduler_loop).start()

app.run(debug=True, host='0.0.0.0', port=5000)