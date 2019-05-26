from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    resp = client.get('/hello')
    assert resp.data == b'Hello, World!'
