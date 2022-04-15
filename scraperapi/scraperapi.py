import queue
import os
import requests
import time
import threading

worker_thread_count = 5

tasks = queue.Queue()

class RequestTask():
    def __init__(self, url: str):
        self.url = url
        self.response = None
        self.finished = False
    
    def run(self):
        params = {'api_key': os.getenv('SCRAPER_API_KEY'), 'url': self.url}
        self.response = requests.get('https://api.scraperapi.com/', params=params)
        self.finished = True

def get_scraperapi_response(url: str):
    task = RequestTask(url)
    tasks.put(task)

    while not task.finished:
        time.sleep(0.1)
    
    return task.response

def worker_thread():
    while True:
        task = tasks.get(block = True)
        task.run()

for i in range(worker_thread_count):
    thread = threading.Thread(target=worker_thread)
    thread.start()