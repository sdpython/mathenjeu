"""
@brief      test tree node (time=1s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from mathenjeu.activities import ActivityGroup
from mathenjeu.cli.cli_helper import build_games


class TestCliHelper(ExtTestCase):

    def test_local_app(self):
        script = "src.mathenjeu.tests.qcms.py:simple_french_qcm,Maths et QCM,0"
        games, fct = build_games(script, None)
        self.assertIsInstance(games, dict)
        self.assertTrue(callable(fct))
        g = fct('simple_french_qcm')
        self.assertIsInstance(g, ActivityGroup)


if __name__ == "__main__":
    unittest.main()
