# -*- coding: utf-8 -*-
"""
@file
@brief Starts an application.
"""
import os
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse, RedirectResponse
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from itsdangerous import URLSafeTimedSerializer
import ujson
from lightmlrestapi.mlapp.base_logging import BaseLogging


class QCMApp(BaseLogging):
    """
    Defines routes for urls. The web application
    can be started with the following code:

    ::

        import uvicorn  # pylint: disable=C0412
        from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
        app2 = QCMApp.create_app(secret_session="dummypwd",
                                 middles=[(ProxyHeadersMiddleware, {})])
        uvicorn.run(app2, host='127.0.0.1', port=8099)

    Module :epkg:`uvicorn` does not implement a secured connection.
    :epkg:`hypercorn` is one alternative.
    """

    def __init__(self, app, secret_key, folder='.',
                 secret_log=None, session_cookie='QCMApp',
                 max_age=14 * 24 * 60 * 60,
                 title=None, secure=False, domain=None, **kwargs):
        """
        @param      app             :epkg:`starlette` application
        @param      secret_key      secret to encrypt the cookie for session,
                                    see :epkg:`SessionMiddleware`
        @param      secret_log      secret for encryption (None to avoid encryption)
        @param      session_cookie  name of the session cookie
        @param      max_age         cookie's like
        @param      folder          folder where to write the logs (None to disable the logging)
        @param      title           title
        @param      domain          domain (where the website is deployed)
        @param      secure          use secured connection for cookies
        @param      kwargs          addition parameter for :epkg:`BaseLogging`
        """
        BaseLogging.__init__(self, secret=secret_log, folder=folder, **kwargs)
        self.app = app
        self.session_cookie = session_cookie
        self.secret_key = secret_key
        self.max_age = max_age
        self.cookie_domain = "127.0.0.1" if domain is None else domain
        self.cookie_path = "/"
        self.signer = URLSafeTimedSerializer(self.secret_key)
        self.title = title if title is not None else "Quelques questions de maths..."
        self.secure = secure

    def log_any(self, tag, msg, request, session=None, **data):
        """
        Logs information.

        @param      tag     tag (to filter rows in logs)
        @param      msg     event kind
        @param      request request
        @param      session information about the session
        @param      data    addition data
        """
        if not session:
            session = self.get_session(request)
        client = request["client"]
        log = dict(msg=msg, session=session, client=client)
        log.update(data)
        self.info(tag, log)

    def log_event(self, msg, request, session=None, **data):
        """
        Logs information about events.

        @param      tag     tag (to filter rows in logs)
        @param      msg     event kind
        @param      request request
        @param      session information about the session
        @param      data    addition data
        """
        self.log_any('[DATA]', msg, request, session=session, **data)

    async def homepage(self, request):
        """
        Defines the main page.
        """
        session = self.get_session(request, notnone=True)
        if 'alias' in session:
            self.log_event("home-logged", request, session=session)
            template = self.app.get_template('index.html')
            content = template.render(
                request=request, title=self.title, **session)
            return HTMLResponse(content)
        else:
            self.log_event("home-unlogged", request, session=session)
            template = self.app.get_template('notlogged.html')
            content = template.render(
                request=request, title=self.title, **session)
            return HTMLResponse(content)

    async def login(self, request):
        """
        Login page.
        """
        template = self.app.get_template('login.html')
        content = template.render(request=request)
        return HTMLResponse(content)

    async def authenticate(self, request):
        """
        Authentification.

        @param      request         request
        @return                     response
        """
        try:
            fo = await request.form()
        except Exception as e:
            raise RuntimeError(
                "Unable to read login and password due to '{0}'".format(e))

        res = self.not_allowed(
            alias=fo['alias'], pwd=fo['pwd'], request=request)
        if res is not None:
            return res
        data = dict(alias=fo['alias'])
        response = RedirectResponse(url='/')
        self.save_session(response, data)
        return response

    def not_allowed(self, alias, pwd, request):
        """
        Checks that a user is allowed.

        @param      user        user
        @param      alias       alias
        """
        if not alias:
            template = self.app.get_template('notauthorized.html')
            content = template.render(request=request, alias=alias)
            return HTMLResponse(content)
        return None

    async def logout(self, request):
        """
        Logout page.
        """
        response = RedirectResponse(url='/')
        response.delete_cookie(self.session_cookie, domain=self.cookie_domain,
                               path=self.cookie_path)
        return response

    def save_session(self, response, data):
        """
        Saves the session to the response in a secure cookie.

        @param      response    response
        @param      data        data
        """
        data = ujson.dumps(data)  # pylint: disable=E1101
        signed_data = self.signer.dumps([data])  # pylint: disable=E1101
        response.set_cookie(self.session_cookie, signed_data,
                            max_age=self.max_age,
                            httponly=True, domain=self.cookie_domain,
                            path=self.cookie_path, secure=self.secure)

    def get_session(self, request, notnone=False):
        """
        Retrieves the session.

        @param      request     request
        @param      notnone     None or empty dictionary
        @return                 session
        """
        cook = request.cookies.get(self.session_cookie)
        if cook is not None:
            unsigned = self.signer.loads(cook)
            data = unsigned[0]
            return ujson.loads(data)  # pylint: disable=E1101
        else:
            return {} if notnone else None

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
        content = template.render(request=request)
        return HTMLResponse(content, status_code=404)

    async def server_error(self, request, exc):
        """
        Returns an :epkg:`HTTP 500` page.
        """
        template = self.app.get_template('500.html')
        content = template.render(request=request)
        return HTMLResponse(content, status_code=500)

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

    @staticmethod
    def create_app(secret_key="test", secret_log=None,
                   session_cookie="mathenjeuqcmapp",
                   folder='.', middles=None, title=None,
                   **kwargs):
        """
        Builds a :epkg:`starlette` application.

        @param      secret_key      secret to encrypt the cookie for session
        @param      secret_log      secret for encryption (None to avoid encryption)
        @param      session_cookie  name of the session cookie
        @param      folder          folder where to write the logs (None to disable the logging)
        @param      middles         list of ``[(middle ward, kwargs)]``
        @param      title           title
        @param      kwargs          see @see cl QCMApp
        """
        if secret_key is None:
            raise ValueError("secret_session cannot be empty.")
        this = os.path.abspath(os.path.dirname(__file__))
        templates = os.path.join(this, "templates")
        if not os.path.exists(templates):
            raise FileNotFoundError("Unable to find '{0}'".format(templates))
        debug = kwargs.pop('debug', False)
        app = Starlette(template_directory=templates, debug=debug)
        if middles is not None:
            for middle, kwargs in middles:
                app.add_middleware(middle, **kwargs)
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1'])
        # app.add_middleware(HTTPSRedirectMiddleware)

        qcm = QCMApp(app, secret_log=secret_log, secret_key=secret_key,
                     session_cookie=session_cookie, folder=folder, title=title,
                     **kwargs)
        statics = os.path.join(this, "statics")
        if not os.path.exists(statics):
            raise FileNotFoundError("Unable to find '{0}'".format(statics))
        app.mount('/static', StaticFiles(directory=statics), name='static')
        app.add_route('/login', qcm.login)
        app.add_route('/logout', qcm.logout)
        app.add_route('/error', qcm.on_error)
        app.add_route('/authenticate', qcm.authenticate, methods=['POST'])
        app.add_exception_handler(404, qcm.not_found)
        app.add_exception_handler(500, qcm.server_error)
        app.add_event_handler("startup", qcm.startup)
        app.add_event_handler("shutdown", qcm.cleanup)
        app.add_route('/', qcm.homepage)
        qcm.info("[QCMApp.create_app] create application", None)
        return app


if __name__ == "__main__":
    import uvicorn  # pylint: disable=C0412
    from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
    app2 = QCMApp.create_app(secret_session="dummypwd",
                             middles=[(ProxyHeadersMiddleware, {})])
    uvicorn.run(app2, host='127.0.0.1', port=8099)
