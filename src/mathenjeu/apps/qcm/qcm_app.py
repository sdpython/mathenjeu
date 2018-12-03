"""
@file
@brief Starts an application.
"""
import os
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from lightmlrestapi.mlapp.base_logging import BaseLogging


class QCMApp(BaseLogging):
    """
    Defines routes for urls.
    """

    def __init__(self, app, secret=None, folder='.', **kwargs):
        """
        @param      app         :epkg:`starlette` application
        @param      secret      secret for encryption (None to avoid encryption)
        @param      folder      folder where to write the logs (None to disable the logging)
        @param      kwargs      addition parameter for :epkg:`BaseLogging`
        """
        BaseLogging.__init__(self, secret=secret, folder=folder, **kwargs)
        self.app = app

    async def homepage(self, request):
        """
        Defines the main page.
        """
        template = self.app.get_template('index.html')
        content = template.render(request=request)
        return HTMLResponse(content)

    async def login(self, request):
        """
        Login page.
        """
        template = self.app.get_template('login.html')
        content = template.render(request=request)
        return HTMLResponse(content)

    async def on_error(self, request):
        """
        An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
        """
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
    def create_app(secret_log=None, secret_session=None, folder='.', **kwargs):
        """
        Builds a :epkg:`starlette` application.

        @param      secret      secret for encryption (None to avoid encryption)
        @param      folder      folder where to write the logs (None to disable the logging)
        @param      kwargs      see @see cl QCMApp
        """
        if secret_session is None:
            raise ValueError("secret_session cannot be empty.")
        this = os.path.abspath(os.path.dirname(__file__))
        templates = os.path.join(this, "templates")
        debug = kwargs.pop('debug', False)
        app = Starlette(template_directory=templates, debug=debug)
        app.add_middleware(ProxyHeadersMiddleware)
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1'])
        # app.add_middleware(HTTPSRedirectMiddleware)
        app.add_middleware(SessionMiddleware, secret_key=secret_session)

        qcm = QCMApp(app, secret=secret_log, folder=folder, **kwargs)
        statics = os.path.join(this, "statics")
        app.mount('/static', StaticFiles(directory=statics), name='static')
        app.add_route('/', qcm.homepage)
        app.add_route('/login', qcm.login)
        app.add_route('/error', qcm.on_error)
        app.add_exception_handler(404, qcm.not_found)
        app.add_exception_handler(500, qcm.server_error)
        app.add_event_handler("startup", qcm.startup)
        app.add_event_handler("shutdown", qcm.cleanup)
        qcm.info("[QCMApp.create_app] create application", None)
        return app
        # hypercorn


if __name__ == "__main__":
    import uvicorn  # pylint: disable=C0412
    app2 = QCMApp.create_app(secret_session="dummypwd")
    uvicorn.run(app2, host='127.0.0.1', port=8099)
