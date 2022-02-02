from app.models import Author

def test_random(app, client):
    val = int(client.get('/random').data)
    assert val >= 0 and val <= 100

def test_createauthor(app, client):
    assert app.session.query(Author).count() == 0
    app.test_client().get('/createauthor')

def test_databaseclear(app, client):
    assert app.session.query(Author).count() == 0
    app.test_client().get('/createauthor')