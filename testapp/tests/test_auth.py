# -*- coding:utf-8 -*-
"""Test file for views."""
import os
import pytest
import webtest 
from testapp import main

@pytest.fixture()
def app():
    settings = {'sqlalchemy.url' : 'postgres://mike:secret@localhost:5432/testing'}
    app = main({}, **settings)
    return webtest.TestApp(app)

@pytest.fixture()
def auth_env():
    os.environ['AUTH_PASSWORD'] = 'secret'
    os.environ['AUTH_USERNAME'] = 'admin'

def test_no_access_to_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403

def test_access_to_view(app):
    response = app.get('/secure')
    assert response.status_code == 200

def test_password_exsists(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None
 
def test_username_exsists(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None