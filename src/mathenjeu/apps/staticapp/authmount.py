"""
@file
@brief Custom Router to check for authentification.
"""
from starlette.responses import RedirectResponse
from starlette.routing import Mount
from starlette.types import ASGIApp, Scope
from starlette.requests import Request


class AuthMount(Mount):
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

    def __call__(self, scope: Scope):
        """
        Checks the user is authenticated, falls back in
        the previous behavior, otherwise redirect to the
        authentification page (``/login``).
        """
        app, session = self.get_app_session(scope)
        if session is not None:
            if app is not None:
                app._log_event("staticpage", scope, session=session)
            alias = session.get('alias', None)
            if alias is not None:
                return Mount.__call__(self, scope)
        # Requires authentification.
        path = scope.get('root_path', '') + '%2F' + scope.get('path', '')
        path = path.replace('/', "%2F")
        return RedirectResponse(url='/login?returnto=' + path)
