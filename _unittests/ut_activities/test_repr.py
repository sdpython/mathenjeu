"""
@brief      test log(time=1s)
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


from src.mathenjeu.activities import Display
from src.mathenjeu.tests import simple_french_qcm


class TestRepr(ExtTestCase):

    def test_repr(self):
        disp = Display(1, 'eid1')
        r = repr(disp)
        self.assertEqual(r, "Display(_col_eid=1, _col_name='eid1')")

    def test_qcm(self):
        test = simple_french_qcm()
        for t in test:
            s = repr(t)
            self.assertStartsWith("QuestionChoice(", s)
            self.assertIn("fr", s)


if __name__ == "__main__":
    unittest.main()
