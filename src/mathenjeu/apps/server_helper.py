"""
@file
@brief Helpers to starts a server.
"""


class Server:
    """
    Defines a server.
    """

    def __init__(self, module="hypercorn", **kwargs):
        """
        @param      module      ``'hypercorn'`` (https) or ``'uvicorn'`` (http)
        @param      kwargs      parameters
        """
        if module == 'hypercorn':
            import hypercorn
            from hypercorn.config import Config
            from hypercorn.run import run
            from hypercorn.utils import load_application
            self.module = hypercorn
            self._run = run
            config = Config()
            app = load_application(kwargs['application_path'])
            if app is None:
                raise RuntimeError("Unable to load application '{0}'".format(
                    kwargs["application_path"]))
        else:
            raise NotImplementedError(
                "Unable to use module '{0}'".format(module))

        for k, v in kwargs.items():
            if k in ('binds',):
                continue
            setattr(config, k, v)

        if len(kwargs['binds']) > 0:
            config.update_bind(kwargs['binds'])
        self.config = config

    @staticmethod
    def create_hypercorn(application_path, secret_key="test", secret_log=None,
                         session_cookie="mathenjeu_QCMApp",
                         access_log="-", access_log_format="%(h)s %(r)s %(s)s %(b)s %(D)s",
                         binds="127.0.0.1:8097", ca_certs=None, certfile=None, debug=False, error_log='-',
                         keep_alive=600, keyfile=None, root_path='', workers=1,
                         reload=False):
        """
        See :epkg:`hypercorn`.

        @param      application_path    path to the application
        @param      secret_key          secret to encrypt the cookie for session
        @param      secret_log          secret for encryption (None to avoid encryption)
        @param      session_cookie      name of the session cookie
        @param      access_log          The target location for the access log, use - for stdout.
        @param      access_log_format   The log format for the access log, see help docs,
                                        see `Logging <https://pgjones.gitlab.io/hypercorn/logging.html>`_.
        @param      binds               The host/address to bind to. Should be either host:port, host, unix:path or fd://num,
                                        e.g. 127.0.0.1:5000, 127.0.0.1, unix:/tmp/socket or fd://33 respectively.
        @param      ca_certs            Path to the SSL CA certificate file.
        @param      certfile            Path to the SSL certificate file.
        @param      ciphers             Ciphers to use for the SSL setup.
        @param      debug               Enable debug mode, i.e. extra logging and checks.
        @param      error_log           The target location for the error log, use - for stderr.
        @param      keep_alive          Seconds to keep inactive connections alive for.
        @param      keyfile             Path to the SSL key file
        @param      root_path           The setting for the ASGI root_path variable.
        @param      workers             The number of workers to spawn and use.
        @param      reload              Enable automatic reloads on code changes.
        """
        kwargs = dict(application_path=application_path, secret_key=secret_key, secret_log=secret_log,
                      session_cookie=session_cookie, access_log=access_log,
                      access_log_format=access_log_format, binds=binds,
                      ca_certs=ca_certs, certfile=certfile, debug=debug, error_log=error_log,
                      keep_alive=keep_alive, keyfile=keyfile, root_path=root_path, workers=workers,
                      reload=reload)
        return Server(module='hypercorn', **kwargs)

    def run(self, verbose=True):
        """
        Starts the server.
        @param      verbose     display the host
        """
        if verbose:
            scheme = "https" if self.config.ssl_enabled else "http"
            print("[mathenjeu] {}: running on {}://{}:{}".format(self.module.__name__,
                                                                 scheme, self.config.host, self.config.port))
        self._run(self.config)


if __name__ == "__main__":
    try:
        import mathenjeu  # pylint: disable=W0611
    except (ModuleNotFoundError, ImportError):
        import sys
        import os
        this = os.path.abspath(os.path.dirname(__file__))
        path = os.path.normpath(os.path.join(this, "..", ".."))
        sys.path.append(path)
        import mathenjeu

    code = """
    '''Starts application.'''
    from mathenjeu.apps import QCMApp  # pylint: disable=E0401
    myapp = QCMApp.create_app(session_cookie="test", secret_key="test")
    """
    with open("test_hypercorn_qcm.py", "w") as f:
        f.write(code.replace("    ", ""))

    server = Server.create_hypercorn(
        "mathenjeu.apps.test_hypercorn_qcm:myapp", debug=True)
    server.run()
