# Explanation of files for /backend
## api/
This directory contains all of the specific Rest API routes defined in .py files for each model (i.e. paper, author, etc.).
## scraping/
This directory contains files specific to allowing the backend to interact with ScraperAPI for the system to be able to scrape Google Scholar.
## static/
This directory contains important styling files such as openapi.yml
## templates/
This directory contains basic HTML that flask serves on its own. Notably this includes SwaggerUI, which allows for API calls without the React frontend.
## test/
This directory contains all files linked to testing the backend of the system (test files, test requirements, etc.)
## Files in this directory
Other files in the backend vary in purpose:
* Files like Dockerfile/requirements.txt are maintained to assist in the setup of the backend of the system.
* All \*.py files are used in the construction of the Flask application (linking routes, creating models, etc.) 
