from flask import Blueprint, current_app, json, request, Flask
from api.models import Task
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
