# -*- coding:utf-8 -*-
"""Test file for views."""
import pytest
import webtest 
from testapp import main

@pytest.fixture()
def app():
    settings = {'sqlalchemy.url' : 'postgres://mike:secret@localhost:5432/testing'}
    app = main({}, **settings)
    return webtest.TestApp(app)

def test_no_access_to_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403

def test_access_to_view(app):
    response = app.get('/secure')
    assert response.status_code == 200