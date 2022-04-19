from typing import Dict
from flask import Blueprint, current_app, json, request, Flask
from api.models import Issue, AmbiguousPaperIssue, CreatePaperTask
from api.templates import db_session, ApiTemplateError
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

@issue_routes.route('/issues/<int:id>', methods=['DELETE'])
def delete_issue(id):
    with db_session(current_app) as session:
        issue = session.query(Issue).get(id)
        if issue is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Issue not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        session.delete(issue)
        return current_app.response_class(
            response=json.dumps({'message': 'Issue deleted',
                                 'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

def resolve_ambiguous_paper_issue(session, issue: AmbiguousPaperIssue, data: Dict):
    correct_scholar_id = data['correct_scholar_id']
            
    if correct_scholar_id is None:
        raise ApiTemplateError('correct_scholar_id is required', 400)
    
    correct_paper = next(filter(lambda paper: paper.scholar_id == correct_scholar_id, issue.paper_choices), None)

    if correct_paper is None:
        raise ApiTemplateError('correct_scholar_id not in paper choices', 400)
    
    create_paper_task = CreatePaperTask(issue.title_query, issue.author_id, correct_scholar_id)
    session.add(create_paper_task)

    session.delete(issue)

@issue_routes.route("/issues/<int:id>/resolve", methods=['POST'])
def resolve_issue(id):
    with db_session(current_app) as session:
        issue = session.query(Issue).get(id)

        if issue is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Issue not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        data = request.get_json()

        try:
            if issue.type == 'ambiguous_paper_issue':
                resolve_ambiguous_paper_issue(session, issue, data)
        except ApiTemplateError as e:
            return current_app.response_class(
                response=json.dumps({'message': e.message,
                                     'status': 'error'}),
                status=e.status,
                mimetype='application/json'
            )

        return current_app.response_class(
            response=json.dumps({'message': 'Issue resolved',
                                 'status': 'success'}),
            status=200,
            mimetype='application/json'
        )