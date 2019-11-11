"""
@file
@brief Starts an app locally to test it.
"""
import os
import sys
import uvicorn
from ..apps import StaticApp
from ..apps.server import ServerHypercorn


def create_static_local_app(
        # log parameters
        secret_log=None,
        folder='.',
        # authentification parameters
        max_age=14 * 24 * 60 * 60,
        cookie_key=None, cookie_name="mathenjeu",
        cookie_domain="127.0.0.1", cookie_path="/",
        # content parameters
        content=None,
        # application parameters
        title="Web Application MathEnJeu", short_title="MathEnJeu",
        page_doc="http://www.xavierdupre.fr/app/mathenjeu/helpsphinx/",
        secure=False, port=8868, middles=None, start=False,
        userpwd=None, debug=False, fLOG=print):
    """
    Creates a local web-application with very simple authentification.

    @param      secret_log      to encrypt log (None to ignore)
    @param      folder          folder where to write the logs (None to disable the logging)

    @param      max_age         cookie's duration in seconds
    @param      cookie_key      to encrypt information in the cookie (cannot be None)
    @param      cookie_name     name of the session cookie
    @param      cookie_domain   cookie is valid for this path only, also defines the
                                domain of the web app (its url)
    @param      cookie_path     path of the cookie once storeds
    @param      secure          use secured connection for cookies
    @param      content         list tuple ``route, folder`` to server or a string
                                ``route1,folder1;route2,folder2;...``

    @param      title           title
    @param      short_title     short application title
    @param      page_doc        page documentation (default is :epkg:`mathenjeu`)
    @param      port            port to deploy the application
    @param      middles         middles ware, list of couple ``[(class, **kwargs)]``
                                where *kwargs* are the parameter constructor
    @param      start           starts the application with :epkg:`uvicorn`
    @param      userpwd         users are authentified with any alias but a common password
    @param      debug           display debug information (:epkg:`starlette` option)
    @param      fLOG            logging function
    @return                     @see cl StaticApp

    .. cmdref::
        :title: Creates a local web-application with very simple authentification
        :cmd: -m mathenjeu static_local --help

        The command line runs a web application meant to be local
        as there is not *https* involved. It serves static content.
        The web app relies on :epkg:`starlette`, the server relies
        on :epkg:`uvicorn`. Example of use::

            python -m mathenjeu static_local --cookie_key=dummypwd --start=1 --port=8889 --userpwd=abc --content=display_name,local_folder

        With that application, every user can login with a unique password *abc*.
    """
    if secret_log == '':
        raise ValueError("secret_log must be not empty or None, not ''")
    if fLOG:
        fLOG("[create_static_local_app] create")

    if isinstance(content, str):
        if fLOG:
            fLOG("[create_static_local_app] parsing '{0}'".format(content))
        content = [tuple(ct.split(',')) for ct in content.split(';')]
        if fLOG:
            fLOG("[create_static_local_app] int {0}".format(content))

    app = StaticApp(secret_log=secret_log, middles=middles,
                    folder=folder, max_age=max_age,
                    cookie_key=cookie_key, cookie_name=cookie_name,
                    cookie_domain=cookie_domain, cookie_path=cookie_path,
                    title=title, short_title=short_title, content=content,
                    secure=secure, page_doc=page_doc, userpwd=userpwd)
    if start:
        if fLOG:
            fLOG(
                "[create_static_local_app] start server 'http://{0}:{1}'".format(cookie_domain, port))
        uvicorn.run(app.app, host=cookie_domain, port=port)
    return app


def create_static_https_app(
        # log parameters
        secret_log=None,
        folder='.',
        # authentification parameters
        max_age=14 * 24 * 60 * 60,
        cookie_key=None, cookie_name="mathenjeu",
        cookie_domain="127.0.0.1", cookie_path="/",
        # application parameters
        title="Web Application MathEnJeu", short_title="MathEnJeu",
        page_doc="http://www.xavierdupre.fr/app/mathenjeu/helpsphinx/",
        secure=False, port=8868, middles=None, start=False,
        userpwd=None, debug=False, content=None,
        # hypercorn parameters
        access_log="-",
        access_log_format="%(h)s %(r)s %(s)s %(b)s %(D)s",
        ca_certs=None, certfile=None, error_log='-',
        keep_alive=600, keyfile=None, root_path='', workers=1,
        reload=False, ciphers="ECDHE+AESGCM", fLOG=print):
    """
    Creates a https web-application with https authentification.

    @param      secret_log          to encrypt log (None to ignore)
    @param      folder              folder where to write the logs (None to disable the logging)

    @param      max_age             cookie's duration in seconds
    @param      cookie_key          to encrypt information in the cookie (cannot be None)
    @param      cookie_name         name of the session cookie
    @param      cookie_domain       cookie is valid for this path only, also defines the
                                    domain of the web app (its url)
    @param      cookie_path         path of the cookie once storeds
    @param      secure              use secured connection for cookies

    @param      title               title
    @param      short_title         short application title
    @param      page_doc            page documentation (default is 'http://www.xavierdupre.fr/app/mathenjeu/helpsphinx')
    @param      port                port to deploy the application
    @param      middles             middles ware, list of couple ``[(class, **kwargs)]``
                                    where *kwargs* are the parameter constructor
    @param      start               starts the application with :epkg:`uvicorn`
    @param      userpwd             users are authentified with any alias but a common password
    @param      debug               display debug information (:epkg:`starlette` option)
    @param      content             list tuple ``route, folder`` to server or a string
                                    ``route1,folder1;route2,folder2;...``

    @param      access_log          The target location for the access log, use - for stdout.
    @param      access_log_format   The log format for the access log, see help docs,
                                    see `Logging <https://pgjones.gitlab.io/hypercorn/logging.html>`_.
    @param      ca_certs            Path to the SSL CA certificate file.
    @param      certfile            Path to the SSL certificate file.
    @param      ciphers             Ciphers to use for the SSL setup, the default can be found at
                                    `config.py <https://github.com/pgjones/hypercorn/blob/master/hypercorn/config.py#L32>`_
    @param      error_log           The target location for the error log, use - for stderr.
    @param      keep_alive          Seconds to keep inactive connections alive for.
    @param      keyfile             Path to the SSL key file
    @param      root_path           The setting for the ASGI root_path variable.
    @param      workers             The number of workers to spawn and use.
    @param      reload              Enable automatic reloads on code changes.
    @param      fLOG                logging function

    @return                         @see cl StaticApp

    .. cmdref::
        :title: Creates a https static web-application with authentification
        :cmd: -m mathenjeu local_https --help

        The command line runs a web application meant to be local
        as there is not :epkg:`https` involved. It servers static content.
        The web app relies on :epkg:`starlette`, the server relies
        on :epkg:`hypercorn`. Example::

            python -m mathenjeu local_https

        With that application, every user can login with a unique password *abc*.
    """
    if secret_log == '':
        raise ValueError("secret_log must be not empty or None, not ''")

    if isinstance(content, str):
        if fLOG:
            fLOG("[create_static_local_app] parsing '{0}'".format(content))
        content = [tuple(ct.split(',')) for ct in content.split(';')]
        if fLOG:
            fLOG("[create_static_local_app] int {0}".format(content))

    kwargs = dict(secret_log=secret_log, middles=middles,
                  folder=folder, max_age=max_age,
                  cookie_key=cookie_key, cookie_name=cookie_name,
                  cookie_domain=cookie_domain, cookie_path=cookie_path,
                  title=title, short_title=short_title,
                  secure=secure, debug=debug, content=content,
                  page_doc=page_doc, userpwd=userpwd)
    app = StaticApp(**kwargs)
    if app.app is None:
        raise RuntimeError("Unable to create a starlette application.")
    if fLOG:
        fLOG("[create_static_https_app] app is created")
    rows = []
    rows.append('"Creates a starlette application."')
    rows.append("from mathenjeu.apps import StaticApp")
    rows.append("kwargs = " + str(kwargs))
    rows.append("app = StaticApp(**kwargs).app")
    name = os.path.join(folder, "apphyper.py")
    with open(name, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))
    if fLOG:
        fLOG("[create_static_https_app] saved file '{0}'".format(name))

    binds = "{0}:{1}".format(cookie_domain, port)
    folder = os.path.abspath(folder)
    sys.path.append(folder)
    try:
        import apphyper  # pylint: disable=C0415
        pa = apphyper.app
        if pa is None:
            raise RuntimeError("pa should not be None")
    except ImportError as e:
        # For unit test purposes.
        from .. import __file__ as mejfile
        main_folder = os.path.abspath(os.path.dirname(mejfile))
        main_folder = os.path.normpath(os.path.join(main_folder, ".."))
        if main_folder not in sys.path:
            sys.path.append(main_folder)
            try:
                import apphyper  # pylint: disable=C0415
                pa = apphyper.app
                if pa is None:
                    raise RuntimeError("pa should not be None")
            except ImportError as e:
                raise ImportError(
                    "Unable to import 'apphyper' from '{0}'\n--sys.path--\n{1}".format(
                        folder, "\n".join(sys.path))) from e
        else:
            raise ImportError(
                "Unable to import 'apphyper' from '{0}'\nFolder '{1}' already present.\n--sys.path--\n{2}".format(
                    folder, main_folder, "\n".join(sys.path))) from e

    application_path = "apphyper:app"
    kwargs = dict(application_path=application_path, access_log=access_log,
                  access_log_format=access_log_format, binds=binds,
                  ca_certs=ca_certs, certfile=certfile, debug=debug, error_log=error_log,
                  keep_alive=keep_alive, keyfile=keyfile, root_path=root_path, workers=workers,
                  reload=reload, ciphers=ciphers)

    if fLOG:
        fLOG("[create_static_https_app] create server")
    server = ServerHypercorn(**kwargs)
    if start:
        if fLOG:
            fLOG(
                "[create_static_https_app] starts server on '{0}'".format(binds))
        server.run()
    while folder in sys.path:
        del sys.path[sys.path.index(folder)]
    return server
