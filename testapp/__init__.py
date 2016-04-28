"""Initialize page and main function."""
import os
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,)
import passlib
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import engine_from_config
from .models import (
    DBSession,
    Base,
)


class MyRoot(object):
    """Custom Root."""
    __acl__= [(Allow, Authenticated, 'secured')]

    def __init__(self, request):
        """Init."""
        self.request = request


def main(global_config, **settings):
    """Function returns a Pyramid WSGI application."""
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'admin')
    settings['auth.password'] = os.environ.get(
        'AUTH_PASSWORD', 'secret')
        
    authn_policy = AuthTktAuthenticationPolicy('itsassecret')
    authz_polciy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_polciy,
        root_factory=MyRoot)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('secure', '/secure')
    config.add_route('entry', '/entry/{id:\d+}')
    config.add_route('new', '/new')
    config.add_route('edit', '/edit/{id:\d+}')
    config.scan()
    config.set_session_factory(sessfac)
    return config.make_wsgi_app()
