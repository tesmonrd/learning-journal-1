# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from testapp.models import DBSession, Base

TEST_DATABASE_URL = 'sqlite:////tmp/test_db.sqlite'

@pytest.fixture(scop - 'session;)')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)