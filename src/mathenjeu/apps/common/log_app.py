# -*- coding: utf-8 -*-
"""
@file
@brief Starts an application.
"""
from lightmlrestapi.mlapp.base_logging import BaseLogging  # pylint: disable=C0411


class LogApp(BaseLogging):
    """
    Defines methods to easily log information for a web application.
    The function *fct_session* returns information
    about the session whatever it is as a dictionary.
    """

    def __init__(self, folder='.', secret_log=None, fct_session=None, **kwargs):
        """
        @param      fct_session     function to return information about a session
        @param      secret_log      to encrypt log (None to ignore)
        @param      folder          folder where to write the logs (None to disable the logging)
        @param      kwargs          additional parameters for :epkg:`BaseLogging`
        """
        BaseLogging.__init__(self, secret=secret_log, folder=folder, **kwargs)
        self.get_session = fct_session

    def log_any(self, tag, msg, request, session=None, **data):
        """
        Logs information.

        @param      tag     tag (to filter rows in logs)
        @param      msg     event kind
        @param      request request
        @param      session information about the session
        @param      data    addition data
        """
        if not session and self.get_session:
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
        if not session and self.get_session:
            session = self.get_session(request)
        self.log_any('[DATA]', msg, request, session=session, **data)
