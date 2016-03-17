# -*- coding:utf-8 -*-
"""Test file for views."""
from testapp.views import entry_view
from testapp.views import home_view
from testapp.models import DBSession, Entry
from pyramid.testing import DummyRequest


def test_entry_view_id(dbtransaction):
    """Test for entry view dictionary title attribute."""
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].title == 'jill'


def test_entry_view_text(dbtransaction):
    """Test for entry view dictionary text attribute."""
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'].text == 'jello'


def test_home_view(dbtransaction):
    """Test home view dictionary title attribute."""
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[0].title == 'jill'


def test_home_view_sort(dbtransaction):
    """Test home view sort functionality via attribute."""
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()
    new_model = Entry(title="two", text='twotext')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    dic = home_view(test_request)
    assert dic['entry_list'].all()[1].title == 'jill'


def test_entry_view(dbtransaction):
    """Test for entry view dictionary is identical to entry instance."""
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()
    test_request = DummyRequest()
    test_request.matchdict = {'id': new_model.id}
    dic = entry_view(test_request)
    assert dic['single_entry'] == new_model
