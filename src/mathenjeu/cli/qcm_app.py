"""
@file
@brief Starts an app locally to test it.
"""
import os
import sys
import uvicorn
from ..apps import QCMApp
from ..apps.server import ServerHypercorn
from .cli_helper import build_games


def create_qcm_local_app(
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
        secure=False, display=None, fct_game=None,
        games="simple_french_qcm,simple_french_qcm,0;ml_french_qcm,ml_french_qcm,0",
        port=8868, middles=None, start=False,
        userpwd=None, debug=False, fLOG=print):
    """
    Creates a local web-application with very simple authentification.

    :param secret_log: to encrypt log (None to ignore)
    :param folder: folder where to write the logs (None to disable the logging)
    :param max_age: cookie's duration in seconds
    :param cookie_key: to encrypt information in the cookie (cannot be None)
    :param cookie_name: name of the session cookie
    :param cookie_domain: cookie is valid for this path only, also defines the
        domain of the web app (its url)
    :param cookie_path: path of the cookie once storeds
    :param secure: use secured connection for cookies
    :param title: title
    :param short_title: short application title
    :param page_doc: page documentation (default is :epkg:`mathenjeu`)
    :param display: display such as @see cl DisplayQuestionChoiceHTML
    :param fct_game: function *lambda name:* @see cl ActivityGroup
    :param games: defines which games is available as a dictionary
        ``{ game_id: (game name, first page id) }`` or
        ``id,name,page;id,name,page``, *id* can be a filename.
    :param port: port to deploy the application
    :param middles: middles ware, list of couple ``[(class, **kwargs)]``
        where *kwargs* are the parameter constructor
    :param start: starts the application with :epkg:`uvicorn`
    :param userpwd: users are authentified with any alias but a common password
    :param debug: display debug information (:epkg:`starlette` option)
    :param fLOG: logging function
    :return: @see cl QCMApp

    .. cmdref::
        :title: Creates a local web-application with very simple authentification
        :cmd: -m mathenjeu qcm_local --help

        The command line runs a web application meant to be local
        as there is not *https* involved. It implements a Q&A.
        The web app relies on :epkg:`starlette`, the server relies
        on :epkg:`uvicorn`. Example of use::

            python -m mathenjeu qcm_local --cookie_key=dummypwd --start=1 --port=8889 --userpwd=abc

        With that application, every user can login with a unique password *abc*.
    """
    if secret_log == '':
        raise ValueError(  # pragma: no cover
            "secret_log must be not empty or None, not ''")
    games, fct_game = build_games(games, fct_game)
    if fLOG:
        fLOG("[create_qcm_local_app] games=" + str(games))

    app = QCMApp(secret_log=secret_log, middles=middles,
                 folder=folder, max_age=max_age,
                 cookie_key=cookie_key, cookie_name=cookie_name,
                 cookie_domain=cookie_domain, cookie_path=cookie_path,
                 title=title, short_title=short_title,
                 secure=secure, display=display, fct_game=fct_game,
                 games=games, page_doc=page_doc, userpwd=userpwd)
    if start:
        if fLOG:
            fLOG(
                "[create_qcm_local_app] start server 'http://{0}:{1}'".format(cookie_domain, port))
        uvicorn.run(app.app, host=cookie_domain, port=port)
    return app


def create_qcm_https_app(
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
        secure=False, display=None,
        games="simple_french_qcm,simple_french_qcm,0;ml_french_qcm,ml_french_qcm,0",
        port=8868, middles=None, start=False,
        userpwd=None, debug=False,
        # hypercorn parameters
        access_log="-",
        access_log_format="%(h)s %(r)s %(s)s %(b)s %(D)s",
        ca_certs=None, certfile=None, error_log='-',
        keep_alive=600, keyfile=None, root_path='', workers=1,
        reload=False, ciphers="ECDHE+AESGCM", fLOG=print):
    """
    Creates a https web-application with https authentification.

    :param secret_log: to encrypt log (None to ignore)
    :param folder: folder where to write the logs (None to disable the logging)
    :param max_age: cookie's duration in seconds
    :param cookie_key: to encrypt information in the cookie (cannot be None)
    :param cookie_name: name of the session cookie
    :param cookie_domain: cookie is valid for this path only, also defines the
        domain of the web app (its url)
    :param cookie_path: path of the cookie once storeds
    :param secure: use secured connection for cookies
    :param title: title
    :param short_title: short application title
    :param page_doc: page documentation (default is 'http://www.xavierdupre.fr/app/mathenjeu/helpsphinx')
    :param display: display such as @see cl DisplayQuestionChoiceHTML
    :param games: defines which games is available as a dictionary
        ``{ game_id: (game name, first page id) }`` or
        ``id,name,page;id,name,page``, *id* can be a filename.
    :param port: port to deploy the application
    :param middles: middles ware, list of couple ``[(class, **kwargs)]``
        where *kwargs* are the parameter constructor
    :param start: starts the application with :epkg:`uvicorn`
    :param userpwd: users are authentified with any alias but a common password
    :param debug: display debug information (:epkg:`starlette` option)

    :param access_log: The target location for the access log, use - for stdout.
    :param access_log_format: The log format for the access log, see help docs,
        see `Logging <https://pgjones.gitlab.io/hypercorn/logging.html>`_.
    :param ca_certs: Path to the SSL CA certificate file.
    :param certfile: Path to the SSL certificate file.
    :param ciphers: Ciphers to use for the SSL setup, the default can be found at
        `config.py <https://github.com/pgjones/hypercorn/blob/master/hypercorn/config.py#L32>`_
    :param error_log: The target location for the error log, use - for stderr.
    :param keep_alive: Seconds to keep inactive connections alive for.
    :param keyfile: Path to the SSL key file
    :param root_path: The setting for the ASGI root_path variable.
    :param workers: The number of workers to spawn and use.
    :param reload: Enable automatic reloads on code changes.
    :param fLOG: logging function
    :return: @see cl QCMApp

    .. cmdref::
        :title: Creates a https web-application (Q&A) with authentification
        :cmd: -m mathenjeu qcm_https --help

        The command line runs a web application meant to be local
        as there is not :epkg:`https` involved. It implements a Q&Q.
        The web app relies on :epkg:`starlette`, the server relies
        on :epkg:`hypercorn`. Example::

            python -m mathenjeu qcm_https

        With that application, every user can login with a unique password *abc*.
    """
    if secret_log == '':
        raise ValueError(  # pragma: no cover
            "secret_log must be not empty or None, not ''")

    games, fct_game = build_games(games, None)
    if fLOG:
        fLOG("[create_qcm_https_app] games=" + str(games))
    kwargs = dict(secret_log=secret_log, middles=middles,
                  folder=folder, max_age=max_age,
                  cookie_key=cookie_key, cookie_name=cookie_name,
                  cookie_domain=cookie_domain, cookie_path=cookie_path,
                  title=title, short_title=short_title,
                  secure=secure, display=display, debug=debug,
                  page_doc=page_doc, userpwd=userpwd)
    app = QCMApp(games=games, fct_game=fct_game, **kwargs)
    if app.app is None:
        raise RuntimeError(  # pragma: no cover
            "Unable to create a starlette application.")
    if fLOG:
        fLOG("[create_qcm_https_app] app is created")
    rows = []
    rows.append('"Creates a starlette application."')
    rows.append("from mathenjeu.cli.cli_helper import build_games")
    rows.append("from mathenjeu.apps import QCMApp")
    rows.append("games = {0}".format(games))
    rows.append("games, fct_game = build_games(games, None)")
    rows.append("kwargs = " + str(kwargs))
    rows.append("app = QCMApp(games=games, fct_game=fct_game, **kwargs).app")
    name = os.path.join(folder, "apphyper.py")
    with open(name, "w", encoding="utf-8") as f:
        f.write("\n".join(rows))
    if fLOG:
        fLOG("[create_qcm_https_app] saved file '{0}'".format(name))

    bind = "{0}:{1}".format(cookie_domain, port)
    folder = os.path.abspath(folder)
    sys.path.append(folder)
    try:
        import apphyper  # pylint: disable=C0415
        pa = apphyper.app
        if pa is None:
            raise RuntimeError("pa should not be None")
    except ImportError as e:  # pragma: no cover
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
                    raise RuntimeError(  # pylint: disable=W0707
                        "pa should not be None")
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
                  access_log_format=access_log_format, bind=bind,
                  ca_certs=ca_certs, certfile=certfile, debug=debug, error_log=error_log,
                  keep_alive=keep_alive, keyfile=keyfile, root_path=root_path, workers=workers,
                  reload=reload, ciphers=ciphers)

    if fLOG:
        fLOG("[create_qcm_https_app] create server")
    server = ServerHypercorn(**kwargs)
    if start:
        if fLOG:  # pragma: no cover
            fLOG("[create_qcm_https_app] starts server on '{0}'".format(bind))
        server.run()
    while folder in sys.path:
        del sys.path[sys.path.index(folder)]
    return server
