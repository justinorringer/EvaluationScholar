from datetime import datetime, timedelta
import pytest
import time

from api.models import Task

timeout = 20

def wait_for_task(session, id):
    start_time = datetime.now()
    while True:
        if session.query(Task).filter(Task.id == id).first() is None:
            return
            
        time.sleep(1)

        if datetime.now() > start_time + timedelta(seconds = timeout):
            pytest.fail("Task not resolved")
        
        session.commit()

def wait_for_task_count(session, target_task_count):
    start_time = datetime.now()
    task_count = session.query(Task).count()
    while True:
        new_task_count = session.query(Task).count()
        if new_task_count == target_task_count:
            return
        
        if new_task_count != task_count:
            task_count = new_task_count
            start_time = datetime.now()
            
        time.sleep(1)

        if datetime.now() > start_time + timedelta(seconds = timeout):
            pytest.fail("Task count not resolved")
        
        session.commit()