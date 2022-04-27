from datetime import datetime
from flask import Blueprint, current_app, json, request, Flask
from api.models import CreatePaperTask, Task, Author
from api.templates import db_session
task_routes = Blueprint('task_routes', __name__, template_folder='templates')

@task_routes.route("/tasks", methods=['GET'])
def get_tasks():
    with db_session(current_app) as session:
        tasks = session.query(Task).all()

        type = request.args.get('type')
        
        if type is not None:
            tasks = [task for task in tasks if task.type == type]
        
        return current_app.response_class(
            response=json.dumps([task.to_dict() for task in tasks]),
            status=200,
            mimetype='application/json'
        )

@task_routes.route("/tasks/<int:id>", methods=['GET'])
def get_task(id):
    with db_session(current_app) as session:
        task = session.query(Task).get(id)
        if task is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Task not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        return current_app.response_class(
            response=json.dumps(task.to_dict()),
            status=200,
            mimetype='application/json'
        )

@task_routes.route("/tasks", methods=['DELETE'])
def delete_tasks():
    with db_session(current_app) as session:
        tasks = session.query(Task).all()

        type = request.args.get('type')

        if type is not None:
            tasks = [task for task in tasks if task.type == type]
        
        for task in tasks:
            session.delete(task)
        
        return current_app.response_class(
            response=json.dumps({'message': 'Tasks deleted',
                                    'status': 'success'}),
                status=200,
                mimetype='application/json'
            )

@task_routes.route("/tasks/<int:id>", methods=['DELETE'])
def delete_task(id):
    with db_session(current_app) as session:
        task = session.query(Task).get(id)
        if task is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Task not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        session.delete(task)
        return current_app.response_class(
            response=json.dumps({'message': 'Task deleted',
                                 'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

@task_routes.route("/tasks/create-papers-list", methods=['POST'])
def create_papers_list():
    with db_session(current_app) as session:
        author_id = request.args.get('author_id')

        if author_id is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Author ID is required',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        if not author_id.isdigit():
            return current_app.response_class(
                response=json.dumps({'message': 'Author ID must be a number',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        author = session.query(Author).get(author_id)

        if author is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Author not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        data = request.get_json()

        if not isinstance(data, list):
            return current_app.response_class(
                response=json.dumps({'message': 'Data must be an array',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )
        
        tasks = []

        for paper_title in data:
            task = CreatePaperTask(paper_title = paper_title, author_id = author_id, date = datetime.now())
            session.add(task)
            session.flush()
            tasks.append(task.to_dict())
        
        return current_app.response_class(
            response=json.dumps(tasks),
                status=201,
                mimetype='application/json'
            )

@task_routes.route("/tasks/create-papers", methods=['POST'])
def create_task():    
    with db_session(current_app) as session:
        author_id = request.args.get('author_id')

        if author_id is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Author ID is required',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        if not author_id.isdigit():
            return current_app.response_class(
                response=json.dumps({'message': 'Author ID must be a number',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        author = session.query(Author).get(author_id)

        if author is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Author not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if 'file' not in request.files:
            return current_app.response_class(
                response=json.dumps({'message': 'File is required',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        tasks = []

        file = request.files['file']
        for line in file:
            task = CreatePaperTask(paper_title = line.decode('utf-8').replace('\n', ''), author_id = author_id, date = datetime.now())
            session.add(task)
            session.flush()
            tasks.append(task.to_dict())
        
        author.uploaded_papers = True

        return current_app.response_class(
            response=json.dumps(tasks),
                status=201,
                mimetype='application/json'
            )