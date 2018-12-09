"""
@file
@brief Starts an app locally to test it.
"""
import uvicorn
from ..apps import QCMApp


def create_local_app(
        # log parameters
        secret_log=None,
        folder='.',
        # authentification parameters
        max_age=14 * 24 * 60 * 60,
        cookie_key=None,
        cookie_name="mathenjeu",
        cookie_domain="127.0.0.1",
        cookie_path="/",
        # application parameters
        title="Web Application MathEnJeu",
        short_title="MathEnJeu",
        page_doc="http://www.xavierdupre.fr/app/mathenjeu/",
        secure=False,
        display=None,
        fct_game=None,
        games=None,
        port=8868,
        middles=None,
        start=False):
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

    @param      title           title
    @param      short_title     short application title
    @param      page_doc        page documentation (default is 'http://www.xavierdupre.fr/app/mathenjeu/')
    @param      display         display such as @see cl DisplayQuestionChoiceHTML
    @param      fct_game        function *lambda name:* @see cl ActivityGroup
    @param      games           defines which games is available as a dictionary
                                ``{ game_id: (game name, first page id) }``
    @param      debug           display debug information (:epkg:`starlette` option)
    @param      middles         middles ware, list of couple ``[(class, **kwargs)]``
                                where *kwargs* are the parameter constructor
    @param      start           starts the application with :epkg:`uvicorn`
    @return                     @see cl QCMApp

    .. cmdref::
        :title: Creates a local web-application with very simple authentification
        :cmd: -m mathenjeu local_webapp --help
    """
    app = QCMApp(secret_log=secret_log, middles=middles,
                 folder=folder, max_age=max_age,
                 cookie_key=cookie_key, cookie_name=cookie_name,
                 cookie_domain=cookie_domain, cookie_path=cookie_path,
                 title=title, short_title=short_title,
                 secure=secure, display=display, fct_game=fct_game,
                 games=games, page_doc=page_doc)
    if start:
        uvicorn.run(app, host=cookie_domain, port=port)
    return app
