# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""
import os
import unittest
from starlette.testclient import TestClient
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from mathenjeu.cli import create_static_local_app


class TestStaticApp(ExtTestCase):

    def test_static_app_empty(self):
        temp = get_temp_folder(__file__, "temp_run_static_app")
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_static_local_app(cookie_key="dummypwd",
                                      folder=temp, middles=middles,
                                      fLOG=None)
        try:
            with TestClient(app.app.router) as client:
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

                page = client.get("/event")
                self.assertEqual(page.status_code, 200)
        except RuntimeError as e:
            if "There is no current event loop in thread" in str(e):
                return
            raise e

    def test_static_app_content(self):
        temp = get_temp_folder(__file__, "temp_run_static_app_content")
        folder = os.path.normpath(os.path.join(temp, '..'))
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_static_local_app(cookie_key="dummypwd",
                                      folder=temp, middles=middles,
                                      content=[('zoo', folder)],
                                      fLOG=None)
        try:
            with TestClient(app.app.router) as client:
                page = client.get("/zoo")
                self.assertEqual(page.status_code, 404)
                page = client.get("/zoo/test_static_app.py")
                self.assertEqual(page.status_code, 200)
                self.assertIn(
                    b'page = client.get("/zoo/test_static_app.py"', page.content)
        except RuntimeError as e:
            if "There is no current event loop in thread" in str(e):
                return
            raise e

    def test_static_app_content_pwd(self):
        temp = get_temp_folder(__file__, "temp_run_static_app_content_pwd")
        folder = os.path.normpath(os.path.join(temp, '..'))
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_static_local_app(cookie_key="dummypwd",
                                      folder=temp, middles=middles,
                                      content=[('zoo', folder)],
                                      userpwd="abcd", fLOG=None)

        try:
            with TestClient(app.app.router) as client:

                page = client.get("/zoo/test_static_app.py")
                self.assertEqual(page.status_code, 200)
                self.assertNotIn(b"assertNotEqual", page.content)
                self.assertIn(b'Login', page.content)

                page = client.get("/zoo")
                self.assertEqual(page.status_code, 200)
                self.assertIn(b'Login', page.content)
        except RuntimeError as e:
            if "There is no current event loop in thread" in str(e):
                return
            raise e


if __name__ == "__main__":
    unittest.main()
