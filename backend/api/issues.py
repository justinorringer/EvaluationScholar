from flask import Blueprint, current_app, json, request, Flask
from api.models import Issue, AmbiguousPaperIssue
from api.templates import db_session
issue_routes = Blueprint('issue_routes', __name__, template_folder='templates')

@issue_routes.route('/issues', methods=['GET'])
def get_issues():
    with db_session(current_app) as session:
        return current_app.response_class(
            response=json.dumps([issue.to_dict() for issue in session.query(Issue).all()]),
            status=200,
            mimetype='application/json'
        )

@issue_routes.route('/issues/<int:id>', methods=['GET'])
def get_issue(id):
    with db_session(current_app) as session:
        issue = session.query(Issue).get(id)
        if issue is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Issue not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        return current_app.response_class(
            response=json.dumps(issue.to_dict()),
            status=200,
            mimetype='application/json'
        )