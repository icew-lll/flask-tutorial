import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    resp = client.post(
        '/auth/register', data={'username': 'a,', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == resp.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user where username = 'a'"
        ).fetchone() is not None


@pytest.mark.parameterize(('username', 'password', 'message'), (
                          ('', '', b'Username is required.'),
                          ('a', '', b'Password is required.'), 
                          ('test', 'test', b'already registered'),
                          ))
def test_register_validate_input(client, username, password, message):
    resp = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in resp.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    resp = auth.login()
    assert resp.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.paramterize(('username', 'password', 'message'),(
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.')
))
def test_login_validate_input(auth, username, password, message):
    resp = auth.login(username, password)
    assert message in resp.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
