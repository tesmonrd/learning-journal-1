# -*- coding:utf-8 -*-
"""Test file for views."""
import os
import pytest
import webtest 
from testapp import main

AUTH_DATA = {'username': 'admin', 'password': 'secret'}

@pytest.fixture()
def app():
    settings = {'sqlalchemy.url' : 'postgres://mike:secret@localhost:5432/testing'}
    app = main({}, **settings)
    return webtest.TestApp(app)

@pytest.fixture()
def auth_env():
    from testapp.security import pwd_context
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'

@pytest.fixture()
def authenticated_app(app,auth_env):
    app.post('/login', AUTH_DATA)
    return app

def test_no_access_to_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403

def test_access_to_view(authenticated_app):
    response = authenticated_app.get('/secure')
    assert response.status_code == 200

def test_password_exsists(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None
 
def test_username_exsists(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None

def test_check_pw_success(auth_env):
    from testapp.security import check_pw
    password = 'secret'
    assert check_pw(password)

def test_stored_password_is_encrypted(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'

def test_get_login_view(app):
    response = app.get('/login')
    response.status_code == 200

def test_post_login_success_redirects_home(app, auth_env):
    response = app.post('/login', AUTH_DATA)
    headers = response.headers
    domain = "http://localhost"
    actual_path = headers.get('Location','')[len(domain):]
    assert actual_path == '/'

def test_post_login_fails(app, auth_env):
    data = {'username': 'admin', 'password': 'not secret'}
    response = app.post('/login', data)
    assert response.status_code == 200

def test_post_login_success_auth_tkt_present(app,auth_env):
    response = app.post('/login', AUTH_DATA)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set 
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False