from flask import Blueprint, current_app, json, request

import scraping
import scraping.scraperapi as scraperapi
import scraping.parsing as parsing
from scraping.errors import ApiNoCreditsError, ApiRequestsFailedError

scraping_routes = Blueprint('scraping_routes', __name__, template_folder='templates')

# Routes to handle interaction with ScraperAPI
# Author(s): Tyler Maxwell, Abhinav Kulhari

@scraping_routes.route('/scraping/profiles', methods=['GET'])
def get_profiles():
    author_name = request.args.get('name')

    try:
        html = scraperapi.search_profile(author_name)
        profiles = parsing.parse_profiles(html)
        profile_json = [{
            'name': parsing.parse_profile_name(profile),
            'institution': parsing.parse_profile_institution(profile),
            'id': parsing.parse_profile_id(profile)
        } for profile in profiles]
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
        response=json.dumps(profile_json),
        status=200,
        mimetype='application/json'
    )

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