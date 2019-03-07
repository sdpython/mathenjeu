# -*- coding: utf-8 -*-
"""
@file
@brief Starts an application.
"""
import os
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Mount
from starlette.templating import Jinja2Templates
from ..common import LogApp, AuthentificationAnswers
from .authmount import AuthMount


class StaticApp(LogApp, AuthentificationAnswers):
    """
    Implements routes for a web application which serves static files
    protected with a password.
    See :ref:`Which server to server starlette application? <faq-server-app-starlette>`.
    The application allows anybody to connect to the website
    assuming the know the password.
    """

    def __init__(self,
                 # log parameters
                 secret_log=None, folder='.',
                 # authentification parameters
                 max_age=14 * 24 * 60 * 60, cookie_key=None,
                 cookie_name="mathenjeu_static",
                 cookie_domain="127.0.0.1",
                 cookie_path="/",
                 # application parameters
                 content=None,
                 title="MathEnJeu - Static Files", short_title="MEJ",
                 page_doc="http://www.xavierdupre.fr/app/mathenjeu/helpsphinx/",
                 secure=False, middles=None, debug=False, userpwd=None):
        """
        @param      secret_log      to encrypt log (None to ignore)
        @param      folder          folder where to write the logs (None to disable the logging)

        @param      max_age         cookie's duration in seconds
        @param      cookie_key      to encrypt information in the cookie (cannot be None)
        @param      cookie_name     name of the session cookie
        @param      cookie_domain   cookie is valid for this path only, also defines the
                                    domain of the web app (its url)
        @param      cookie_path     path of the cookie once storeds
        @param      secure          use secured connection for cookies
        @param      content         list tuple ``route, folder`` to server

        @param      title           title
        @param      short_title     short application title
        @param      middles         middles ware, list of couple ``[(class, **kwargs)]``
                                    where *kwargs* are the parameter constructor
        @param      userpwd         users are authentified with any alias but a common password
        @param      debug           display debug information (:epkg:`starlette` option)
        """
        if title is None:
            raise ValueError("title cannot be None.")
        if short_title is None:
            raise ValueError("short_title cannot be None.")

        this = os.path.abspath(os.path.dirname(__file__))
        templates = os.path.join(this, "templates")
        statics = os.path.join(this, "statics")
        if not os.path.exists(statics):
            raise FileNotFoundError("Unable to find '{0}'".format(statics))
        if not os.path.exists(templates):
            raise FileNotFoundError("Unable to find '{0}'".format(templates))

        login_page = "login.html"
        notauth_page = "notauthorized.html"
        redirect_logout = "/"
        app = Starlette(debug=debug)

        AuthentificationAnswers.__init__(self, app, login_page=login_page,
                                         notauth_page=notauth_page, redirect_logout=redirect_logout,
                                         max_age=max_age, cookie_name=cookie_name, cookie_key=cookie_key,
                                         cookie_domain=cookie_domain, cookie_path=cookie_path,
                                         page_context=self.page_context, userpwd=userpwd)
        LogApp.__init__(self, folder=folder, secret_log=secret_log,
                        fct_session=self.get_session)

        self.title = title
        self.short_title = short_title
        self.page_doc = page_doc
        self.approutes = []
        self.templates = Jinja2Templates(directory=templates)

        if middles is not None:
            for middle, kwargs in middles:
                app.add_middleware(middle, **kwargs)
        app.add_middleware(TrustedHostMiddleware,
                           allowed_hosts=[cookie_domain])
        # app.add_middleware(HTTPSRedirectMiddleware)

        app.mount('/static', StaticFiles(directory=statics), name='static')
        app.add_route('/login', self.login)
        app.add_route('/logout', self.logout)
        app.add_route('/error', self.on_error)
        app.add_route('/authenticate', self.authenticate, methods=['POST'])
        app.add_exception_handler(404, self.not_found)
        app.add_exception_handler(500, self.server_error)
        app.add_route('/', self.main)
        app.add_route('/event', self.event)
        app.add_event_handler("startup", self.startup)
        app.add_event_handler("shutdown", self.cleanup)
        self.info("[StaticApp.create_app] create application", None)

        impossible = {'static', 'login', 'error', 'logout',
                      'authenticate', 'startup', 'shutdown'}

        if content is not None:
            for route, local_folder in content:
                route = route.strip()
                if not os.path.exists(local_folder):
                    raise FileNotFoundError(
                        "Unable to find folder '{0}' mapped to '{1}'".format(local_folder, route))
                if route in impossible:
                    raise ValueError(
                        "Route '{0}' is forbidden (cannot be in {1})".format(route, impossible))
                st = StaticFiles(directory=local_folder)
                if userpwd:
                    rt = AuthMount('/' + route, app=st, name=route)
                else:
                    rt = Mount('/' + route, app=st, name=route)
                app.router.routes.append(rt)

                index = os.path.join(local_folder, 'index.html')
                if os.path.exists(index):
                    self.approutes.append(
                        (route, '/{}/index.html'.format(route)))
                else:
                    res = os.listdir(local_folder)
                    found = False
                    for r in res:
                        full = os.path.join(local_folder, r)
                        if os.path.isfile(full):
                            self.approutes.append(
                                (route, '/{}/{}'.format(route, r)))
                            found = True
                            break
                    if not found:
                        self.approutes.append((route, '/' + route))

    #########
    # common
    #########

    def page_context(self, **kwargs):
        """
        Returns the page context before applying any template.

        @param      kwargs      arguments
        @return                 parameters
        """
        res = dict(title=self.title, short_title=self.short_title,
                   page_doc=self.page_doc, approutes=self.approutes)
        res.update(kwargs)
        return res

    def startup(self):
        """
        Startups.
        """
        self.info('[StaticApp] startup', None)

    def cleanup(self):
        """
        Cleans up.
        """
        self.info('[StaticApp] cleanup', None)

    def unlogged_response(self, request, session):
        """
        Returns an answer for somebody looking to access
        the questions without being authentified.
        """
        self.log_event("home-unlogged", request, session=session)
        context = {'request': request}
        context.update(self.page_context(**session))
        return self.templates.TemplateResponse('notlogged.html', context)

    ########
    # route
    ########

    async def main(self, request):
        """
        Defines the main page.
        """
        session = self.get_session(request, notnone=True)
        if 'alias' in session:
            self.log_event("home-logged", request, session=session)
            context = {'request': request}
            context.update(self.page_context(**session))
            return self.templates.TemplateResponse('index.html', context)
        else:
            return self.unlogged_response(request, session)

    async def on_error(self, request):
        """
        An example error.
        """
        self.log_any('[error]', "?", request)
        raise RuntimeError("Oh no")

    async def not_found(self, request, exc):
        """
        Returns an :epkg:`HTTP 404` page.
        """
        context = {'request': request}
        context.update(self.page_context())
        return self.templates.TemplateResponse('404.html', context, status_code=404)

    async def server_error(self, request, exc):
        """
        Returns an :epkg:`HTTP 500` page.
        """
        context = {'request': request}
        context.update(self.page_context())
        return self.templates.TemplateResponse('500.html', context, status_code=500)

    #########
    # event route
    #########

    async def event(self, request):
        """
        This route does not return anything interesting except
        a blank page, but it logs
        """
        session = self.get_session(request, notnone=True)
        ps = request.query_params
        tostr = ','.join('{0}:{1}'.format(k, v) for k, v in sorted(ps.items()))
        self.log_event("event", request, session=session, events=[tostr])
        return PlainTextResponse("")
