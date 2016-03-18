from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
    )
from wtforms import Form, BooleanField, TextField, validators
import markdown


class EntryForm(Form):
    new_title = TextField('Title', [validators.Length(min=4, max=128)])
    new_text = TextField('Content', [validators.Length(min=6)])
    submit = SubmitField('Submit',)

@view_config(route_name='home', renderer='templates/list.jinja2')
def home_view(request):
    try:
        entry_list = DBSession.query(Entry).order_by(Entry.id.desc())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'entry_list': entry_list}


@view_config(route_name='entry', renderer='templates/detail.jinja2')
def entry_view(request):
    try:
        # entry_id = '{id}'.format(**request.matchdict)
        entry_id = request.matchdict['id']
        single_entry = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'single_entry': single_entry}


# @view_config(route_name='add_entry', renderer='template/add.jinja2')
# def new_entry(request):
#     try:
#         pass
#     except:


# @view_config(route_name='edit_entry', renderer='template/edit.jinja2')
# def edit_view(request):
#     try:
#         pass
#     except:
        



conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_testapp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
