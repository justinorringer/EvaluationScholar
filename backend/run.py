from factory import create_app, create_connection_string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from api.models import Base, User
from datetime import timedelta
import time

from multiprocessing import Process
import os

engine = create_engine(create_connection_string(), echo=False)

while True:
    try:
        engine.connect()
        break
    except:
        time.sleep(5)

Session = sessionmaker(bind=engine)
app = create_app(scoped_session(Session))
Base.metadata.create_all(engine)

from task_manager import TaskManager
task_manager = TaskManager(connection_string = create_connection_string(), max_concurrent_tasks = 5)
p = Process(target=task_manager.scheduler_loop)
p.start()

session = Session()
session.query(User).delete()

authorized_users = os.environ.get('AUTHORIZED_USERS')

if authorized_users is None:
    print('WARNING: No authorized users')
else:
    for user in authorized_users.split(','):
        session.add(User(shib_uid=user))

session.commit()
session.close()

app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)