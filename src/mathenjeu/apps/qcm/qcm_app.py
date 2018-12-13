# -*- coding: utf-8 -*-
"""
@file
@brief Starts an application.
"""
import os
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, RedirectResponse, PlainTextResponse
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from ..common import LogApp, AuthentificationAnswers
from ..display import DisplayQuestionChoiceHTML
from ...tests import get_game


class QCMApp(LogApp, AuthentificationAnswers):
    """
    Implements routes for a web application.
    Module :epkg:`uvicorn` does not implement a secured connection.
    :epkg:`hypercorn` is one alternative.
    """

    def __init__(self,
                 # log parameters
                 secret_log=None, folder='.',
                 # authentification parameters
                 max_age=14 * 24 * 60 * 60, cookie_key=None,
                 cookie_name="mathenjeu", cookie_domain="127.0.0.1",
                 cookie_path="/",
                 # application parameters
                 title="Web Application MathEnJeu", short_title="MathEnJeu",
                 page_doc="http://www.xavierdupre.fr/app/mathenjeu/",
                 secure=False, display=None, fct_game=None, games=None,
                 middles=None, debug=False, userpwd=None):
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

        @param      title           title
        @param      short_title     short application title
        @param      page_doc        documentation page
        @param      display         display such as @see cl DisplayQuestionChoiceHTML (default value)
        @param      fct_game        function *lambda name:* @see cl ActivityGroup
        @param      games           defines which games is available as a dictionary
                                    ``{ game_id: (game name, first page id) }``
        @param      middles         middles ware, list of couple ``[(class, **kwargs)]``
                                    where *kwargs* are the parameter constructor
        @param      userpwd         users are authentified with any alias but a common password
        @param      debug           display debug information (:epkg:`starlette` option)
        """
        if title is None:
            raise ValueError("title cannot be None.")
        if short_title is None:
            raise ValueError("short_title cannot be None.")
        if display is None:
            display = DisplayQuestionChoiceHTML()
        if fct_game is None:
            fct_game = get_game
        if games is None:
            games = dict(test_qcm1=('Maths', 0))

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
        app = Starlette(template_directory=templates, debug=debug)

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
        self.display = display
        self.get_game = fct_game
        self.games = games

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
        app.add_route('/answer', self.answer, methods=['POST', 'GET'])
        app.add_exception_handler(404, self.not_found)
        app.add_exception_handler(500, self.server_error)
        app.add_event_handler("startup", self.startup)
        app.add_event_handler("shutdown", self.cleanup)
        app.add_route('/', self.main)
        app.add_route('/qcm', self.qcm)
        app.add_route('/last', self.lastpage)
        app.add_route('/event', self.event)
        self.info("[QCMApp.create_app] create application", None)

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
                   page_doc=self.page_doc)
        res.update(kwargs)
        return res

    def startup(self):
        """
        Startups.
        """
        self.info('[QCMApp] startup', None)

    def cleanup(self):
        """
        Cleans up.
        """
        self.info('[QCMApp] cleanup', None)

    def unlogged_response(self, request, session):
        """
        Returns an answer for somebody looking to access
        the questions without being authentified.
        """
        self.log_event("home-unlogged", request, session=session)
        template = self.app.get_template('notlogged.html')
        content = template.render(
            request=request, **self.page_context(**session))
        return HTMLResponse(content)

    def unknown_game(self, request, session):
        """
        Returns an answer for somebody looking to access
        the questions without being authentified.
        """
        self.log_event("home-nogame", request, session=session)
        template = self.app.get_template('nogame.html')
        content = template.render(
            request=request, **self.page_context(**session))
        return HTMLResponse(content)

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
            template = self.app.get_template('index.html')
            content = template.render(
                request=request, **self.page_context(games=self.games, **session))
            return HTMLResponse(content)
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
        template = self.app.get_template('404.html')
        content = template.render(request=request, **self.page_context())
        return HTMLResponse(content, status_code=404)

    async def server_error(self, request, exc):
        """
        Returns an :epkg:`HTTP 500` page.
        """
        template = self.app.get_template('500.html')
        content = template.render(request=request, **self.page_context())
        return HTMLResponse(content, status_code=500)

    async def qcm(self, request):
        """
        Defines the main page.
        """
        session = self.get_session(request, notnone=True)
        if 'alias' in session:
            game = request.query_params.get('game', None)
            if game is None:
                return self.unknown_game(request, session)
            else:
                obj_game = self.get_game(game)
                if isinstance(obj_game, str):
                    raise RuntimeError(
                        "obj_game for '{0}' cannot be string".format(game))
                qn = request.query_params.get('qn', 0)
                data = dict(game=game, qn=qn)
                events = request.query_params.get('events', None)
                if events:
                    data['events'] = events
                self.log_event("qcm", request, session=session, **data)
                template = self.app.get_template('qcm.html')
                disp = self.display
                context = disp.get_context(obj_game, qn)
                context.update(session)
                context['game'] = game
                if events:
                    context['events'] = events
                content = template.render(
                    request=request, **self.page_context(**context))
                return HTMLResponse(content)
        else:
            return self.unlogged_response(request, session)

    async def answer(self, request):
        """
        Captures an answer.

        @param      request         request
        @return                     response
        """
        try:
            fo = await request.form()
        except Exception as e:
            raise RuntimeError(
                "Unable to read answer due to '{0}'".format(e))
        session = self.get_session(request, notnone=True)
        ps = request.query_params
        fo.update(ps)
        self.log_event("answer", request, session=session, data=fo)
        if 'next' in fo and fo['next'] in (None, 'None'):
            response = RedirectResponse(url='/last?game=' + fo['game'])
        else:
            response = RedirectResponse(
                url='/qcm?game={0}&qn={1}'.format(fo.get('game', ''), fo.get('next', '')))
        return response

    async def lastpage(self, request):
        """
        Defines the last page.
        """
        session = self.get_session(request, notnone=True)
        template = self.app.get_template('lastpage.html')
        ps = request.query_params
        self.log_event("finish", request, session=session, data=ps)
        content = template.render(request=request, alias=session.get('alias'),
                                  **self.page_context())
        return HTMLResponse(content)

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
