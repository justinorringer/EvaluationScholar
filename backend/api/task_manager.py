from flask import Blueprint, current_app, json, request
from sqlalchemy import desc

from api.models import Variable
from api.templates import db_session

task_manager_routes = Blueprint('task_manager_routes', __name__, template_folder='templates')

@task_manager_routes.route('/task_manager/update_period', methods=['GET'])
def get_update_period():
    with db_session(current_app) as session:
        variable = session.query(Variable).filter(Variable.name == "citation_update_period").first()

        if not variable:
            variable = Variable("citation_update_period", "3")
            session.add(variable)
        
        return current_app.response_class(
            response=json.dumps({"value": variable.value}),
            status=200,
            mimetype='application/json'
        )

@task_manager_routes.route('/task_manager/update_period', methods=['PUT'])
def update_update_period():
    with db_session(current_app) as session:
        data = request.get_json()

        if not data['value']:
            return current_app.response_class(
                response=json.dumps({'message': 'no value provided',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        if not data['value'].isdigit():
            return current_app.response_class(
                response=json.dumps({'message': 'value must be a number',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )
        
        if int(data['value']) < 1:
            return current_app.response_class(
                response=json.dumps({'message': 'value must be greater than 0',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        variable = session.query(Variable).filter(Variable.name == "citation_update_period").first()

        if not variable:
            variable = Variable("citation_update_period", data['value'])
            session.add(variable)
        else:
            variable.value = data['value']

        return current_app.response_class(
            response=json.dumps({'message': 'update period updated',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )