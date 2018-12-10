"""
@brief      test tree node (time=7s)
"""


import sys
import os
import unittest
from pyquickhelper.pycode import ExtTestCase

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

from src.mathenjeu.activities import ActivityGroup
from src.mathenjeu.cli.cli_helper import build_games


class TestCliHelper(ExtTestCase):

    def test_src_import(self):
        """for pylint"""
        self.assertTrue(src is not None)

    def test_local_app(self):
        script = "src.mathenjeu.tests.qcms.py:simple_french_qcm,Maths et QCM,0"
        games, fct = build_games(script, None)
        self.assertIsInstance(games, dict)
        self.assertTrue(callable(fct))
        g = fct('simple_french_qcm')
        self.assertIsInstance(g, ActivityGroup)


if __name__ == "__main__":
    unittest.main()
