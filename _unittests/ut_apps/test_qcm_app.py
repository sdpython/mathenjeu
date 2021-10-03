# -*- coding: utf-8 -*-
"""
@brief      test log(time=33s)
"""
import unittest
from starlette.testclient import TestClient
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from mathenjeu.cli import create_qcm_local_app


class TestQcmApp(ExtTestCase):

    def test_qcm_app(self):
        temp = get_temp_folder(__file__, "temp_run_qcm_app")
        middles = [(ProxyHeadersMiddleware, {})]
        app = create_qcm_local_app(cookie_key="dummypwd",
                                   folder=temp, middles=middles)
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
        except RuntimeError as e:
            if "There is no current event loop in thread" in str(e):
                return
            raise e


if __name__ == "__main__":
    unittest.main()
