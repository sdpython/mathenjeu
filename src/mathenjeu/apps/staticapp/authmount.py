"""
@file
@brief Custom Router to check for authentification.
"""
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.types import ASGIApp, Scope, Receive, Send


class _CommonMethods:

    def get_app_session(self, scope):
        """
        Retrieves the :epkg:`starlette` application and
        the session.

        @param      scope       request
        @return                 application, session
        """
        app = scope.get('app', None)
        if app is None:
            return None, None
        request = Request(scope)  # , receive=receive)
        session = app._get_session(request)
        return app, session


class AuthMount(Mount, _CommonMethods):
    """
    The router checks for authentification by looking for a cookie
    which contains an alias. This alias can only be set if the user
    was able to authentify himself.
    """

    def __init__(self, path: str, app: ASGIApp, name: str = None) -> None:
        """
        @param  path    application mapped to this path
        @param  app     application
        @param  name    name
        """
        Mount.__init__(self, path=path, app=app, name=name)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Checks the user is authenticated, falls back in
        the previous behavior, otherwise redirect to the
        authentification page (``/login``).
        """
        redirect = True
        app, session = self.get_app_session(scope)
        if session is not None:
            if app is not None:
                app._log_event("staticpage", scope, session=session)
            alias = session.get('alias', None)
            if alias is not None:
                await Mount.__call__(self, scope, receive, send)
                redirect = False
        if redirect:
            # Requires authentification.
            path = scope.get('root_path', '') + '%2F' + scope.get('path', '')
            path = path.replace('/', "%2F")
            resp = RedirectResponse(url='/login?returnto=' + path)
            await resp(scope, receive, send)


class AuthStaticFiles(StaticFiles, _CommonMethods):
    """
    Overloads *StaticFiles* to check authentification.
    """

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        The ASGI entry point.
        """
        redirect = True
        app, session = self.get_app_session(scope)
        if session is not None:
            if app is not None:
                app._log_event("staticpage", scope, session=session)
            alias = session.get('alias', None)
            if alias is not None:
                await Mount.__call__(self, scope, receive, send)
                redirect = False
        if redirect:
            # Requires authentification.
            path = scope.get('root_path', '') + '%2F' + scope.get('path', '')
            path = path.replace('/', "%2F")
            resp = RedirectResponse(url='/login?returnto=' + path)
            await resp(scope, receive, send)
        else:
            assert scope["type"] == "http"

            if not self.config_checked:
                await self.check_config()
                self.config_checked = True

            path = self.get_path(scope)
            response = await self.get_response(path, scope)
            await response(scope, receive, send)
