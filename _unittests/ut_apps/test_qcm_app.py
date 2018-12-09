# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""

import sys
import os
import unittest
from starlette.testclient import TestClient
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from pyquickhelper.pycode import get_temp_folder, ExtTestCase


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.mathenjeu.cli import create_local_app


class TestQcmApp(ExtTestCase):

    def test_qcm_app(self):
        temp = get_temp_folder(__file__, "temp_run_qcm_app")
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_local_app(cookie_key="dummypwd",
                               folder=temp, middles=middles)
        client = TestClient(app.app.router)
        page = client.get("/")
        self.assertNotEqual(page.status_code, 400)
        self.assertIn(b"MathJax.Hub.Config", page.content)
        self.assertIn(b"MathEnJeu", page.content)

        page = client.get("/login")
        self.assertNotEqual(page.status_code, 400)
        self.assertIn(b"MathEnJeu", page.content)

        page = client.get("/logout")
        self.assertNotEqual(page.status_code, 400)
        self.assertIn(b"MathEnJeu", page.content)

        page = client.get("/authenticate")
        self.assertNotEqual(page.status_code, 400)

        self.assertRaise(lambda: client.get("/error"), RuntimeError)

        page = client.get("/qcm")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"MathEnJeu", page.content)

        page = client.get("/last")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"MathEnJeu", page.content)

        page = client.get("/event")
        self.assertEqual(page.status_code, 200)

        page = client.get("/answer")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"MathEnJeu", page.content)


if __name__ == "__main__":
    unittest.main()
