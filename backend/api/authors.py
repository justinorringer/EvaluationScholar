from flask import Blueprint, current_app, json, request, Flask
from sqlalchemy import func
from sqlalchemy.orm import subqueryload
from api.models import Author, Paper, Tag
from api.templates import db_session
author_routes = Blueprint('author_routes', __name__, template_folder='templates')

# Routes to handle CRUD actions for the Author model
# Author(s): Tyler Maxwell, Abhinav Kulhari

@author_routes.route('/authors', methods=['GET'])
def get_authors():
    with db_session(current_app) as session:
        includes = request.args['include'].split(',') if 'include' in request.args else []
        authors = session.query(Author).options(subqueryload(Author.papers).subqueryload(Paper.citations))
        
        if 'name' in request.args:
            words = request.args['name'].split()
            for word in words:
                authors = authors.filter(Author.name.ilike(f'%{word}%'))
        
        if 'tags' in request.args:
            tags_ids = request.args['tags'].split(',')
            # Could use a for loop and filter multiple times, but that does a join for each tag
            # Instead, do a single join and count the number of tags that match, checking if the count is equal to the number of tags in the request
            authors = authors.join(Author.tags).filter(Tag.id.in_(tags_ids)).group_by(Author.id).having(func.count(Tag.id) >= len(tags_ids))
        
        authors = authors.all()

        if 'min-i10' in request.args:
            try:
                authors = [author for author in authors if author.get_i10_index() >= int(request.args['min-i10'])]
            except ValueError:
                return json.dumps({'error': 'min-i10 must be an integer'}), 400
        
        if 'max-i10' in request.args:
            try:
                authors = [author for author in authors if author.get_i10_index() <= int(request.args['max-i10'])]
            except ValueError:
                return json.dumps({'error': 'max-i10 must be an integer'}), 400
        
        if 'min-h' in request.args:
            try:
                authors = [author for author in authors if author.get_h_index() >= int(request.args['min-h'])]
            except ValueError:
                return json.dumps({'error': 'min-h must be an integer'}), 400
        
        if 'max-h' in request.args:
            try:
                authors = [author for author in authors if author.get_h_index() <= int(request.args['max-h'])]
            except ValueError:
                return json.dumps({'error': 'max-h must be an integer'}), 400

        return current_app.response_class(
            response=json.dumps([author.to_dict(includes) for author in authors]),
            status=200,
            mimetype='application/json'
        )

@author_routes.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    with db_session(current_app) as session:
        includes = request.args['include'].split(',') if 'include' in request.args else []
        author = session.query(Author).get(id)
        if author is None:
            return current_app.response_class(
                response=json.dumps({'message': 'Author not found',
                                     'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
    
        return current_app.response_class(
            response=json.dumps(author.to_dict(includes)),
            status=200,
            mimetype='application/json'
        )
        
@author_routes.route('/authors', methods=['POST'])
def create_author():
    with db_session(current_app) as session:
        data = request.get_json()

        if data is None:
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
        if 'scholar_id' not in data:
            return current_app.response_class(
                response=json.dumps({'message': 'missing scholar_id',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        if data['scholar_id'] is not None and session.query(Author).filter(Author.scholar_id == data['scholar_id']).first() is not None:
            return current_app.response_class(
                response=json.dumps({'message': 'duplicate scholar_id',
                                     'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        author = Author(name=data['name'], scholar_id=data['scholar_id'])
        session.add(author)
        session.flush()
        return current_app.response_class(
            response=json.dumps(author.to_dict()),
            status=201,
            mimetype='application/json'
        )

@author_routes.route('/authors/<int:id>', methods=['PUT'])
def update_author(id):
    with db_session(current_app) as session:
        data = request.get_json()
        author = session.query(Author).get(id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'Author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if 'name' in data:
            author.name = data['name']
        if 'institution' in data:
            author.institution = data['institution']
        if 'scholar_id' in data:
            author.scholar_id = data['scholar_id']    

        return current_app.response_class(
            response=json.dumps({'message': 'author updated',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )
        

@author_routes.route('/authors/<int:id>', methods=['DELETE'])
def delete_author(id):
    with db_session(current_app) as session:
        author = session.query(Author).get(id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        session.delete(author)
        return current_app.response_class(
            response=json.dumps({'message': 'author deleted',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )
        

@author_routes.route('/authors/<int:author_id>/papers/<int:paper_id>', methods=['PUT'])
def add_paper_to_author(author_id, paper_id):
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

        if paper in author.papers:
            return current_app.response_class(
                response=json.dumps({'message': 'paper already added',
                                    'status': 'error'}),
                status=400,
                mimetype='application/json'
            )

        author.papers.append(paper)
        return current_app.response_class(
            response=json.dumps({'message': 'paper added to author',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

@author_routes.route('/authors/<int:author_id>/papers/<int:paper_id>', methods=['DELETE'])
def remove_paper_from_author(author_id, paper_id):
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

        author.papers.remove(paper)
        return current_app.response_class(
            response=json.dumps({'message': 'paper removed from author',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

@author_routes.route('/authors/<int:author_id>/papers', methods=['GET'])
def get_papers_by_author(author_id):
    with db_session(current_app) as session:
        includes = request.args['include'].split(',') if 'include' in request.args else []
        author = session.query(Author).options(subqueryload(Author.papers).subqueryload(Paper.citations))
        author = author.get(author_id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        return current_app.response_class(
            response=json.dumps([paper.to_dict(includes ) for paper in author.papers]),
            status=200,
            mimetype='application/json'
        )

# Tag list routes

@author_routes.route('/authors/<int:author_id>/tags', methods=['GET'])
def get_tags_by_author(author_id):
    with db_session(current_app) as session:
        author = session.query(Author).get(author_id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )
            
        return current_app.response_class(
            response=json.dumps([tag.to_dict() for tag in author.tags]),
            status=200,
            mimetype='application/json'
        )

@author_routes.route('/authors/<int:author_id>/tags/<int:tag_id>', methods=['PUT'])
def add_tag_to_author(author_id, tag_id):
    with db_session(current_app) as session:
        author = session.query(Author).get(author_id)
        tag = session.query(Tag).get(tag_id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if not tag:
            return current_app.response_class(
                response=json.dumps({'message': 'tag not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if tag not in author.tags:
            author.tags.append(tag)
        
        return current_app.response_class(
            response=json.dumps({'message': 'tag added to author',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

@author_routes.route('/authors/<int:author_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_author(author_id, tag_id):
    with db_session(current_app) as session:
        author = session.query(Author).get(author_id)
        tag = session.query(Tag).get(tag_id)

        if not author:
            return current_app.response_class(
                response=json.dumps({'message': 'author not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if not tag:
            return current_app.response_class(
                response=json.dumps({'message': 'tag not found',
                                    'status': 'error'}),
                status=404,
                mimetype='application/json'
            )

        if tag in author.tags:
            author.tags.remove(tag)
        
        return current_app.response_class(
            response=json.dumps({'message': 'tag removed from author',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )


@author_routes.route('/authors/tags', methods=['PUT'])
def batch_add_tags():
    with db_session(current_app) as session:
        data = request.get_json()
        authors = session.query(Author).filter(Author.id.in_(data['authors']))
        tags = session.query(Tag).filter(Tag.id.in_(data['tags']))

        for author in authors:
            for tag in tags:
                if tag not in author.tags:
                    author.tags.append(tag)

        return current_app.response_class(
            response=json.dumps({'message': 'tags added to authors',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )

@author_routes.route('/authors/tags', methods=['DELETE'])
def batch_remove_tags():
    with db_session(current_app) as session:
        data = request.get_json()
        authors = session.query(Author).filter(Author.id.in_(data['authors']))
        tags = session.query(Tag).filter(Tag.id.in_(data['tags']))

        for author in authors:
            for tag in tags:
                if tag in author.tags:
                    author.tags.remove(tag)

        return current_app.response_class(
            response=json.dumps({'message': 'tags removed from authors',
                                    'status': 'success'}),
            status=200,
            mimetype='application/json'
        )