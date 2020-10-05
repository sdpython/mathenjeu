# -*- coding: utf-8 -*-
"""
@file
@brief Starts an application.
"""
import hashlib
from starlette.responses import RedirectResponse
from itsdangerous import URLSafeTimedSerializer
import ujson


class AuthentificationAnswers:
    """
    Defines answers for an application with authentification.
    It stores a cookie with only the user alias.
    The method `authentify_user <mathenjeu.apps.common.auth_app.AuthentificationAnswers.authentify_user>`_
    must be overwritten. The method
    `page_context <mathenjeu.apps.qcm.acm_app.ACMApp.page_context>`_
    returns additional information to add before applying any template.
    """

    def __init__(self, app,
                 login_page="login.html",
                 notauth_page="notauthorized.html",
                 auth_page="authorized.html",
                 redirect_logout="/", max_age=14 * 24 * 60 * 60,
                 cookie_key=None, cookie_name="mathenjeu",
                 cookie_domain="127.0.0.1", cookie_path="/",
                 secure=False, page_context=None, userpwd=None):
        """
        @param      app             :epkg:`starlette` application
        @param      login_page      name of the login page
        @param      notauth_page    page displayed when a user is not authorized
        @param      auth_page       page displayed when a user is authorized
        @param      redirect_logout a not authorized used is redirected to this page
        @param      max_age         cookie's duration in seconds
        @param      cookie_key      to encrypt information in the cookie (cannot be None)
        @param      cookie_name     name of the session cookie
        @param      cookie_domain   cookie is valid for this path only
        @param      cookie_path     path of the cookie once storeds
        @param      secure          use secured connection for cookies
        @param      page_context    to retrieve additional context
                                    before rendering the pages (as a function
                                    which returns a dictionary)
        @param      userpwd         users are authentified with any alias but a common password
        """
        if cookie_key is None:
            raise ValueError("cookie_key cannot be None")
        self.app = app
        self.login_page = login_page
        self.notauth_page = notauth_page
        self.auth_page = auth_page
        self.redirect_logout = redirect_logout
        self.cookie_name = cookie_name
        self.cookie_domain = cookie_domain
        self.cookie_path = cookie_path
        self.cookie_key = cookie_key
        self.max_age = max_age
        self.secure = secure
        self.signer = URLSafeTimedSerializer(self.cookie_key)
        self.userpwd = userpwd
        self.hashed_userpwd = None if userpwd is None else self.hash_pwd(
            userpwd)
        self._get_page_context = page_context
        app._get_session = self.get_session
        for method in ['log_event', 'log_any']:
            if hasattr(self, method):
                setattr(app, '_' + method, getattr(self, method))

    async def login(self, request):
        """
        Login page. If paramater *returnto* is specified in the url,
        the user will go to this page after being logged.
        """
        ps = request.query_params
        context = {'request': request, 'returnto': ps.get('returnto', '/')}
        context.update(self._get_page_context())
        return self.templates.TemplateResponse(self.login_page, context)  # pylint: disable=E1101

    def hash_pwd(self, pwd):
        """
        Hashes a password.

        @param      pwd     password
        @return             hashed password in hexadecimal format
        """
        m = hashlib.sha256()
        m.update(pwd.encode("utf-8"))
        return m.hexdigest()

    async def authenticate(self, request):
        """
        Authentification.

        @param      request         request
        @return                     response
        """
        try:
            fo = await request.form()
        except Exception as e:
            raise RuntimeError(  # pylint: disable=W0707
                "Unable to read login and password due to '{0}'".format(e))
        if 'alias' not in fo:
            return self.is_allowed(
                alias=None, pwd=None, request=request)

        ps = request.query_params
        loge = getattr(self, 'logevent', None)
        if loge:
            loge("authenticate", request, session={},  # pylint: disable=E1102
                 alias=fo['alias'])
        res = self.is_allowed(alias=fo['alias'], pwd=fo['pwd'],
                              request=request)
        if res is not None:
            return res
        data = dict(alias=fo['alias'], hashpwd=self.hash_pwd(fo['pwd']))
        returnto = ps.get('returnto', '/')
        context = {'request': request,
                   'alias': fo['alias'], 'returnto': returnto}
        context.update(self._get_page_context())
        response = self.templates.TemplateResponse(  # pylint: disable=E1101
            'authorized.html', context)
        self.save_session(response, data)
        return response
        # response = RedirectResponse(url=returnto)
        # return response

    async def logout(self, request):
        """
        Logout page.
        """
        response = RedirectResponse(url=self.redirect_logout)
        response.delete_cookie(self.cookie_name, domain=self.cookie_domain,
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
        response.set_cookie(self.cookie_name, signed_data,
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
        cook = request.cookies.get(self.cookie_name)
        if cook is not None:
            unsigned = self.signer.loads(cook)
            data = unsigned[0]
            jsdata = ujson.loads(data)  # pylint: disable=E1101
            # We check the hashed password is still good.
            hashpwd = jsdata.get('hashpwd', '')
            if not self.authentify_user(jsdata.get('alias', ''), hashpwd, False):
                # We cancel the authentification.
                return {}
            return jsdata
        return {} if notnone else None

    def is_allowed(self, alias, pwd, request):
        """
        Checks that a user is allowed. Returns None if it is allowed,
        otherwise an page with an error message.

        @param      alias       alias or iser
        @param      pwd         password
        @param      request     received request
        @return                 None if allowed, *HTMLResponse* otherwise
        """
        if not self.authentify_user(alias, pwd):
            context = {'request': request, 'alias': alias}
            context.update(self._get_page_context())
            return self.templates.TemplateResponse('notauthorized.html', context)  # pylint: disable=E1101
        return None

    def authentify_user(self, alias, pwd, hash_before=True):
        """
        Overwrites this method to allow or reject users.

        @param      alias       alias or user
        @param      pwd         password
        @param      hash_before hashes the password before comparing, otherwise,
                                the function assumes it is already hashed
        @return                 boolean

        The current behavior is to allow anybody if the alias is longer
        than 3 characters.
        """
        if alias is None or len(alias.strip()) <= 3:
            return False
        if self.hashed_userpwd is None:
            return True
        if hash_before:
            hashed_pwd = self.hash_pwd(pwd)
            return hashed_pwd == self.hashed_userpwd
        return pwd == self.hashed_userpwd
