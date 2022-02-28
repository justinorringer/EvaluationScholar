## Team 6 Project

### Building

Docker and docker-compose are required to build this project. To build, run `docker-compose up`.

This will create and run two containers: the MySQL database and the Flask app. The application can be accessed from localhost:5000.

### Code Changes

While in debug mode, Flask will automatically detect changes to the project code and rerun the app.

### Testing

From the `backend/test` directory, install the testing requirements with `pip install -r requirements.txt`

To run the tests, run `python -m pytest` from `backend`.