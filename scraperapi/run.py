from flask import Flask, request, jsonify, current_app
from scraperapi import get_scraperapi_response

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    if 'url' not in request.args:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = request.args['url']

    response = get_scraperapi_response(url)

    return current_app.response_class(
        response = response.text,
        status = response.status_code,
        mimetype='text/html'
    )

app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)