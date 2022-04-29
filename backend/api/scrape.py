from flask import Blueprint, current_app, json, request

from scraping import scrape_profiles, scrape_papers
from scraping.google_scholar import get_profile_page_html, parse_profile_page
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

@scraping_routes.route('/scraping/profiles/<string:scholar_id>', methods=['GET'])
def get_profile_page(scholar_id):
    try:
        html = get_profile_page_html(scholar_id)
        profile = parse_profile_page(html)

        if "all_papers" in request.args and request.args["all_papers"] == "true":
            for page in range(2, 10):
                html = get_profile_page_html(scholar_id, page)
                papers = parse_profile_page(html)["papers"]

                if len(papers) == 0:
                    break
                else:
                    profile["papers"] += papers
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
        response=json.dumps(profile),
        status=200,
        mimetype='application/json'
    )