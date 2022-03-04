from flask import Blueprint, current_app, json, request

import scraping
from scraping.errors import ApiNoCreditsError, ApiRequestsFailedError

scraping_routes = Blueprint('scraping_routes', __name__, template_folder='templates')

# Routes to handle interaction with ScraperAPI
# Author(s): Tyler Maxwell, Abhinav Kulhari

@scraping_routes.route('/scraping/papers', methods=['GET'])
def scrape_paper():
    paper_title = request.args.get('title')

    try:
        citation_count, year = scraping.scrape_paper(paper_title)
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
    
    if citation_count is None or year is None:
        return current_app.response_class(
            response=json.dumps({'message': 'failed to scrape',
                                 'status': 'error'}),
            status=500,
            mimetype='application/json'
        )
    
    return current_app.response_class(
        response=json.dumps({'citation_count': citation_count, 'year': year,}),
        status=200,
        mimetype='application/json'
    )