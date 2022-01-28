from app import app

import random

#API routes

@app.route('/random', methods=['GET'])
def rand():
    return str(random.randint(1, 100))