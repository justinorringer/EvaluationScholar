from factory import create_app, create_connection_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from api.models import Base
from datetime import timedelta

from multiprocessing import Process

engine = create_engine(create_connection_string(), echo=False)

Session = sessionmaker(bind=engine)
app = create_app(scoped_session(Session))
Base.metadata.create_all(engine)

from task_manager import TaskManager
task_manager = TaskManager(timedelta(seconds = 1), timedelta(seconds = 1), create_connection_string())
p = Process(target=task_manager.scheduler_loop)
p.start()

app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)