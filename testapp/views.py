from pyramid.response import Response
from pyramid.view import view_config
import transaction
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    Entry,
)
from wtforms import Form, StringField, TextField, validators
from pyramid.httpexceptions import HTTPFound
# import markdown


class EntryForm(Form):
    """Define EntryForm class."""

    title = StringField('Title', [validators.Length(min=4, max=128,
                                  message='Title must be 4 to 128 characters long')])
    text = TextField('Content', [validators.Length(min=6)])


@view_config(route_name='new', renderer='templates/add.jinja2')
def new_entry(request):
    """Create a form page for a new entry."""
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        entry_id = new_entry.id
        transaction.commit()
        return HTTPFound(location='entry/{}'.format(entry_id))
    return {'form': form}


@view_config(route_name='edit', renderer='templates/add.jinja2')
def edit_entry(request):
    """Create a form page for an edited entry."""
    edit_id = request.matchdict['id']
    edit_entry = DBSession.query(Entry).get(edit_id)
    form = EntryForm(request.POST, edit_entry)
    if request.method == "POST" and form.validate():
        form.populate_obj(edit_entry)
        DBSession.add(edit_entry)
        DBSession.flush()
        entry_id = edit_entry.id
        transaction.commit()
        return HTTPFound(location='/entry/{}'.format(entry_id))
    return {'form': form}


@view_config(route_name='home', renderer='templates/list.jinja2')
def home_view(request):
    """Render home page with database list."""
    try:
        entry_list = DBSession.query(Entry).order_by(Entry.id.desc())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'entry_list': entry_list}


@view_config(route_name='entry', renderer='templates/detail.jinja2')
def entry_view(request):
    """Render a single page detailed view of an entry."""
    try:
        entry_id = request.matchdict['id']
        single_entry = DBSession.query(Entry).filter(Entry.id == entry_id).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'single_entry': single_entry}


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
