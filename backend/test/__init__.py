from datetime import datetime, timedelta
import pytest
import time

from api.models import Task

timeout = 20

def wait_for_task(task_manager, id):
    start_time = datetime.now()
    while True:
        if task_manager.get_task_done(id):
            return
            
        time.sleep(1)

        if datetime.now() > start_time + timedelta(seconds = timeout):
            pytest.fail("Task not resolved")

def wait_for_task_count(task_manager, target_task_count):
    start_time = datetime.now()
    task_count = task_manager.get_total_task_count()
    while True:
        new_task_count = task_manager.get_total_task_count()
        if new_task_count == target_task_count:
            return
        
        if new_task_count != task_count:
            task_count = new_task_count
            start_time = datetime.now()
            
        time.sleep(1)

        if datetime.now() > start_time + timedelta(seconds = timeout):
            pytest.fail("Task count not resolved")