from flask import Blueprint, current_app, json, request
from sqlalchemy import desc

from app.api.models import Author, Citation, Paper
from scraping import scrape_citations, ApiNoCreditsError, ApiRequestsFailedError

from datetime import datetime

paper_routes = Blueprint('paper_routes', __name__, template_folder='templates')

# Routes starting with /api/papers

# Not sure if we need a list of all the papers saved in the databse
@paper_routes.route('/api/papers', methods=['GET'])
def get_papers():
    return current_app.response_class(
        response=json.dumps([paper.to_dict() for paper in current_app.session.query(Paper).all()]),
        status=200,
        mimetype='application/json'
    )

@paper_routes.route('/api/papers/<int:id>', methods=['GET'])
def get_paper(id):
    paper = current_app.session.query(Paper).get(id)

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

@paper_routes.route('/api/papers', methods=['POST'])
def create_paper():
    data = request.get_json()
    paper = Paper(data['name'], data['year'])
    current_app.session.add(paper)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps(paper.to_dict()),
        status=201,
        mimetype='application/json'
    )  

@paper_routes.route('/api/papers/<int:id>', methods=['PUT'])
def update_paper(id):
    data = request.get_json()
    paper = current_app.session.query(Paper).get(id)

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

    current_app.session.commit()

    return current_app.response_class(
        response=json.dumps({'message': 'paper updated',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

@paper_routes.route('/api/papers/<int:id>', methods=['DELETE'])
def delete_paper(id):
    paper = current_app.session.query(Paper).get(id)

    if not paper:
        return current_app.response_class(
            response=json.dumps({'message': 'paper not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    current_app.session.delete(paper)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps({'message': 'paper deleted',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

# Not sure if we want to add an author to a paper
@paper_routes.route('/api/papers/<int:paper_id>/authors/<int:author_id>', methods=['PUT'])
def add_author_to_paper(author_id, paper_id):
    author = current_app.session.query(Author).get(author_id)
    paper = current_app.session.query(Paper).get(paper_id)

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

    paper.authors.append(author)
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps({'message': 'author added to paper',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

# Not sure if we want to remove an author from a paper
@paper_routes.route('/api/papers/<int:paper_id>/authors/<int:author_id>', methods=['DELETE'])
def remove_author_from_paper(author_id, paper_id):
    author = current_app.session.query(Author).get(author_id)
    paper = current_app.session.query(Paper).get(paper_id)

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
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps({'message': 'author removed from paper',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )  

@paper_routes.route('/api/papers/<int:paper_id>/authors', methods=['GET'])
def get_authors_in_paper(paper_id):
    paper = current_app.session.query(Paper).get(paper_id)
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

@paper_routes.route('/api/papers/<int:paper_id>/citations', methods=['GET'])
def get_citations(paper_id):
    paper = current_app.session.query(Paper).get(paper_id)
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

@paper_routes.route('/api/papers/<int:paper_id>/latest-citations', methods=['GET'])
def get_latest_citations(paper_id):
    paper = current_app.session.query(Paper).get(paper_id)
    if not paper:
        return current_app.response_class(
            response=json.dumps({'message': 'paper not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    latest = current_app.session.query(Citation).order_by(desc('date')).first()

    return current_app.response_class(
        response=json.dumps(latest),
        status=200,
        mimetype='application/json'
    )

@paper_routes.route('/api/papers/<int:paper_id>/citations', methods=['POST'])
def new_citation(paper_id):
    paper = current_app.session.query(Paper).get(paper_id)
    if not paper:
        return current_app.response_class(
            response=json.dumps({'message': 'paper not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )
    
    try:
        citation_count = scrape_citations(paper.name)
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
    current_app.session.commit()
    return current_app.response_class(
        response=json.dumps(json.dumps(citation.to_dict())),
        status=200,
        mimetype='application/json'
    )

@paper_routes.route('/api/papers/citations', methods=['POST'])        
def new_citation_multiple_papers():

    created_citations = []
    status_code = 200

    for paper_id in request.get_json():
        print(request.get_json())
        paper = current_app.session.query(Paper).get(paper_id)

        if not paper:
            continue

        try:
            citation_count = scrape_citations(paper.name)
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
        current_app.session.commit()
        created_citations.append(citation.to_dict())
    
    return current_app.response_class(
        response=json.dumps(json.dumps(created_citations)),
        status=status_code,
        mimetype='application/json'
    )