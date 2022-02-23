from flask import Blueprint, current_app, json, request
from sqlalchemy import desc

from api.models import Tag, Author

tag_routes = Blueprint('tag_routes', __name__, template_folder='templates')

# Routes starting with /api/tags

@tag_routes.route('/tags', methods=['POST'])
def create_tag():
    data = request.get_json()

    if not data['name']:
        return current_app.response_class(
            response=json.dumps({'message': 'no name provided',
                                 'status': 'error'}),
            status=400,
            mimetype='application/json'
        )

    tag = Tag(name=data['name'])
    current_app.session.add(tag)
    current_app.session.commit()

    return current_app.response_class(
        response=json.dumps(tag.to_dict()),
        status=201,
        mimetype='application/json'
    )

@tag_routes.route('/tags', methods=['GET'])
def get_tags():
    return current_app.response_class(
        response=json.dumps([tag.to_dict() for tag in current_app.session.query(Tag).all()]),
        status=200,
        mimetype='application/json'
    )

@tag_routes.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = current_app.session.query(Tag).get(tag_id)

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )
    
    return current_app.response_class(
        response=json.dumps(tag.to_dict()),
        status=200,
        mimetype='application/json'
    )

@tag_routes.route('/tags/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    data = request.get_json()

    tag = current_app.session.query(Tag).get(tag_id)

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if data['name']:
        tag.name = data['name']

    current_app.session.commit()

    return current_app.response_class(
        response=json.dumps({'message': 'paper updated',
                                'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

@tag_routes.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = current_app.session.query(Tag).get(tag_id)

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    current_app.session.delete(tag)
    current_app.session.commit()

    return current_app.response_class(
        response=json.dumps({'message': 'tag deleted',
                             'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

# Author list routes

@tag_routes.route('/tags/<int:tag_id>/authors', methods=['GET'])
def get_tag_authors(tag_id):
    tag = current_app.session.query(Tag).get(tag_id)

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    return current_app.response_class(
        response=json.dumps([author.to_dict() for author in tag.authors]),
        status=200,
        mimetype='application/json'
    )

@tag_routes.route('/tags/<int:tag_id>/authors/<int:author_id>', methods=['PUT'])
def add_author_to_tag(tag_id, author_id):
    tag = current_app.session.query(Tag).get(tag_id)

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    author = current_app.session.query(Author).get(author_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if author not in tag.authors:
        tag.authors.append(author)
        current_app.session.commit()

    return current_app.response_class(
        response=json.dumps({'message': 'author added to tag',
                             'status': 'success'}),
        status=200,
        mimetype='application/json'
    )

@tag_routes.route('/tags/<int:tag_id>/authors/<int:author_id>', methods=['DELETE'])
def remove_author_from_tag(tag_id, author_id):
    tag = current_app.session.query(Tag).get(tag_id)

    if not tag:
        return current_app.response_class(
            response=json.dumps({'message': 'tag not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    author = current_app.session.query(Author).get(author_id)

    if not author:
        return current_app.response_class(
            response=json.dumps({'message': 'author not found',
                                 'status': 'error'}),
            status=404,
            mimetype='application/json'
        )

    if author in tag.authors:
        tag.authors.remove(author)
        current_app.session.commit()

    return current_app.response_class(
        response=json.dumps({'message': 'author removed from tag',
                             'status': 'success'}),
        status=200,
        mimetype='application/json'
    )