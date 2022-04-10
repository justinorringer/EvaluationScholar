from flask import Blueprint, current_app, json, request
from sqlalchemy import desc

from api.models import Author, Citation, Paper, UpdateCitationsTask
from scraping import scrape_papers
from scraping.errors import ApiNoCreditsError, ApiRequestsFailedError
from api.templates import db_session

from datetime import datetime
import math

# Routes to handle CRUD actions for the Paper model
# Author(s): Tyler Maxwell, Abhinav Kulhari

paper_routes = Blueprint('paper_routes', __name__, template_folder='templates')

# Routes starting with /api/papers

# Not sure if we need a list of all the papers saved in the databse
@paper_routes.route('/papers', methods=['GET'])
def get_papers():
    with db_session(current_app) as session:
        papers = session.query(Paper)

        total_objects = papers.count()

        custom_headers = {}

        if 'limit' in request.args:
            try:
                limit = int(request.args['limit'])
            except ValueError:
                return json.dumps({'error': 'Invalid limit'}), 400
            
            if limit < 1:
                return json.dumps({'error': 'Invalid limit'}), 400
            
            papers = papers.limit(limit)
            total_pages = 1 if total_objects == 0 else int(math.ceil(total_objects / limit))

            if 'page' in request.args:
                try:
                    page = int(request.args['page'])
                except ValueError:
                    return json.dumps({'error': 'Invalid page'}), 400
                
                if page < 1:
                    return json.dumps({'error': 'Invalid page'}), 400

                if page > total_pages:
                    return json.dumps({'error': 'Page too far'}), 404

                papers = papers.offset(limit * (page - 1))
            
            custom_headers['Total-Pages'] = total_pages

        papers = papers.all()

        return current_app.response_class(
            response=json.dumps([paper.to_dict() for paper in papers]),
            status=200,
            headers=custom_headers,
            mimetype='application/json'
        )

@paper_routes.route('/papers/<int:id>', methods=['GET'])
def get_paper(id):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(id)

        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        return current_app.response_class(
            response=json.dumps(paper.to_dict()),
            status=200,
            mimetype='application/json'
        )    

@paper_routes.route('/papers', methods=['POST'])
def create_paper():
    with db_session(current_app) as session:
        data = request.get_json()

        if not data:
            return current_app.response_class(
                response=json.dumps({'message': 'invalid request body',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )
        
        if 'name' not in data:
            return current_app.response_class(
                response=json.dumps({'message': 'missing name',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )
        
        if 'year' not in data:
            return current_app.response_class(
                response=json.dumps({'message': 'missing year',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        if session.query(Paper).filter(Paper.name == data['name']).first():
            return current_app.response_class(
                response=json.dumps({'message': 'duplicate paper name',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        paper = Paper(data['name'], data['year'])
        session.add(paper)
        session.flush()
        return current_app.response_class(
            response=json.dumps(paper.to_dict()),
            status=201,
            mimetype='application/json'
        )  

@paper_routes.route('/papers/<int:id>', methods=['PUT'])
def update_paper(id):
    with db_session(current_app) as session:
        data = request.get_json()
        paper = session.query(Paper).get(id)

        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'Paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if 'name' in data:
            paper.name = data['name']
        if 'year' in data:
            paper.year = data['year']

        return current_app.response_class(
            response=json.dumps({'message': 'paper updated',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

@paper_routes.route('/papers/<int:id>', methods=['DELETE'])
def delete_paper(id):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(id)

        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        update_citation_tasks = session.query(UpdateCitationsTask).filter(UpdateCitationsTask.paper_id == id).all()

        for task in update_citation_tasks:
            session.delete(task)
        session.delete(paper)

        return current_app.response_class(
            response=json.dumps({'message': 'paper deleted',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

# Not sure if we want to add an author to a paper
@paper_routes.route('/papers/<int:paper_id>/authors/<int:author_id>', methods=['PUT'])
def add_author_to_paper(author_id, paper_id):
    with db_session(current_app) as session:
        author = session.query(Author).get(author_id)
        paper = session.query(Paper).get(paper_id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if author in paper.authors:
            return current_app.response_class(
                response=json.dumps({'message': 'author already in paper',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        paper.authors.append(author)
        return current_app.response_class(
            response=json.dumps({'message': 'author added to paper',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

# Not sure if we want to remove an author from a paper
@paper_routes.route('/papers/<int:paper_id>/authors/<int:author_id>', methods=['DELETE'])
def remove_author_from_paper(author_id, paper_id):
    with db_session(current_app) as session:
        author = session.query(Author).get(author_id)
        paper = session.query(Paper).get(paper_id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        paper.authors.remove(author)
        return current_app.response_class(
            response=json.dumps({'message': 'author removed from paper',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )  

@paper_routes.route('/papers/<int:paper_id>/authors', methods=['GET'])
def get_authors_in_paper(paper_id):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(paper_id)
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        return current_app.response_class(
            response=json.dumps([author.to_dict() for author in paper.authors]),
            status=200,
            mimetype='application/json'
        )

@paper_routes.route('/papers/<int:paper_id>/citations', methods=['GET'])
def get_citations(paper_id):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(paper_id)
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        return current_app.response_class(
            response=json.dumps([citation.to_dict() for citation in paper.citations]),
            status=200,
            mimetype='application/json'
        )

@paper_routes.route('/papers/<int:paper_id>/latest-citations', methods=['GET'])
def get_latest_citations(paper_id):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(paper_id)
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        latest = session.query(Citation).order_by(desc('date')).first()

        return current_app.response_class(
            response=json.dumps(latest.to_dict()),
            status=200,
            mimetype='application/json'
        )

@paper_routes.route('/papers/<int:paper_id>/citations', methods=['POST'])
def new_citation(paper_id):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(paper_id)
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        
        try:
            papers = scrape_papers(paper.name)
            citation_count = papers[0]['citations']
        except ApiNoCreditsError:
            return current_app.response_class(
                response=json.dumps({'message': 'API credits exceeded',
                                    'status': 'error'}),
                status=403,
                mimetype='application/json'
            )
        except ApiRequestsFailedError:
            return current_app.response_class(
                response=json.dumps({'message': 'failed to scrape citations',
                                    'status': 'error'}),
                status=500,
                mimetype='application/json'
            )

        if citation_count == None:
            return current_app.response_class(
                response=json.dumps({'message': 'paper title not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        
        citation = Citation(citation_count, datetime.now())
        paper.citations.append(citation)
        session.flush()
        return current_app.response_class(
            response=json.dumps(citation.to_dict()),
            status=200,
            mimetype='application/json'
        )

@paper_routes.route('/papers/<int:paper_id>/citations/<int:citation_count>', methods=['POST'])
def new_citation_with_count(paper_id, citation_count):
    with db_session(current_app) as session:
        paper = session.query(Paper).get(paper_id)
        if not paper:
            return current_app.response_class(
                response=json.dumps({'message': 'paper not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        
        # try:
        #     citation_count = scrape_citations(paper.name)
        # except ApiNoCreditsError:
        #     return current_app.response_class(
        #         response=json.dumps({'message': 'API credits exceeded',
        #                              'status': 'error'}),
        #         status=403,
        #         mimetype='application/json'
        #     )
        # except ApiRequestsFailedError:
        #     return current_app.response_class(
        #         response=json.dumps({'message': 'failed to scrape citations',
        #                              'status': 'error'}),
        #         status=500,
        #         mimetype='application/json'
        #     )

        if citation_count == None:
            return current_app.response_class(
                response=json.dumps({'message': 'invalid citation count',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
        
        citation = Citation(citation_count, datetime.now())
        paper.citations.append(citation)
        return current_app.response_class(
            response=json.dumps(citation.to_dict()),
            status=200,
            mimetype='application/json'
        )


@paper_routes.route('/papers/citations', methods=['POST'])        
def new_citation_multiple_papers():
    with db_session(current_app) as session:
        created_citations = []
        status_code = 200

        for paper_id in request.get_json():
            print(request.get_json())
            paper = session.query(Paper).get(paper_id)

            if not paper:
                continue

            try:
                papers = scrape_papers(paper.name)
                citation_count = papers[0]['citations']
            except ApiNoCreditsError:
                return current_app.response_class(
                    response=json.dumps(json.dumps(created_citations)),
                    status=403,
                    mimetype='application/json'
                )
            except ApiRequestsFailedError:
                status_code = 500
                continue

            if citation_count == None:
                continue
                
            citation = Citation(citation_count, datetime.now())
            paper.citations.append(citation)
            created_citations.append(citation.to_dict())
        
        return current_app.response_class(
            response=created_citations,
            status=status_code,
            mimetype='application/json'
        )