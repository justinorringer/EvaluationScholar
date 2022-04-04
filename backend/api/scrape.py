from flask import Blueprint, current_app, json, request

from scraping import scrape_profiles, scrape_papers
from scraping.errors import ApiNoCreditsError, ApiRequestsFailedError

scraping_routes = Blueprint('scraping_routes', __name__, template_folder='templates')

# Routes to handle interaction with ScraperAPI
# Author(s): Tyler Maxwell, Abhinav Kulhari

@scraping_routes.route('/scraping/profiles', methods=['GET'])
def get_profiles():
    author_name = request.args.get('name')

    try:
        profiles = scrape_profiles(author_name)
    except ApiNoCreditsError:
        return current_app.response_class(
            response=json.dumps({'message': 'API credits exceeded',
                                 'status': 'error'}),
            status=403,
            mimetype='application/json'
        )
    except ApiRequestsFailedError:
        return current_app.response_class(
            response=json.dumps({'message': 'failed to scrape',
                                 'status': 'error'}),
            status=500,
            mimetype='application/json'
        )
    
    return current_app.response_class(
        response=json.dumps(profiles),
        status=200,
        mimetype='application/json'
    )

@scraping_routes.route('/scraping/papers', methods=['GET'])
def scrape_paper():
    paper_title = request.args.get('title')

    try:
        papers = scrape_papers(paper_title)
    except ApiNoCreditsError:
        return current_app.response_class(
            response=json.dumps({'message': 'API credits exceeded',
                                 'status': 'error'}),
            status=403,
            mimetype='application/json'
        )
    except ApiRequestsFailedError:
        return current_app.response_class(
            response=json.dumps({'message': 'failed to scrape',
                                 'status': 'error'}),
            status=500,
            mimetype='application/json'
        )
    
    return current_app.response_class(
        response=json.dumps(papers),
        status=200,
        mimetype='application/json'
    )