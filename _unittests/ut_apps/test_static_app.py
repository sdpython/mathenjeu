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

        page = client.get("/event")
        self.assertEqual(page.status_code, 200)

    def test_static_app_content(self):
        temp = get_temp_folder(__file__, "temp_run_static_app_content")
        folder = os.path.normpath(os.path.join(temp, '..'))
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_static_local_app(cookie_key="dummypwd",
                                      folder=temp, middles=middles,
                                      content=[('zoo', folder)])
        client = TestClient(app.app.router)
        page = client.get("/zoo")
        self.assertEqual(page.status_code, 404)
        page = client.get("/zoo/test_static_app.py")
        self.assertEqual(page.status_code, 200)
        self.assertIn(
            b'page = client.get("/zoo/test_static_app.py"', page.content)

    def test_static_app_content_pwd(self):
        temp = get_temp_folder(__file__, "temp_run_static_app_content_pwd")
        folder = os.path.normpath(os.path.join(temp, '..'))
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_static_local_app(cookie_key="dummypwd",
                                      folder=temp, middles=middles,
                                      content=[('zoo', folder)],
                                      userpwd="abc")
        client = TestClient(app.app.router)
        page = client.get("/zoo")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Login', page.content)
        page = client.get("/zoo/test_static_app.py")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b'Login', page.content)


if __name__ == "__main__":
    unittest.main()
