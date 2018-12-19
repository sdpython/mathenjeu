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


from src.mathenjeu.tests import simple_french_qcm, ml_french_qcm


class TestaTestsctivityGroup(ExtTestCase):

    def test_qcm(self):
        test = simple_french_qcm()
        for t in test:
            s = repr(t)
            self.assertStartsWith("QuestionChoice(", s)
            self.assertIn("fr", s)
        r = repr(test)
        self.assertStartsWith("ActivityGroup(_col_acts=[", r)
        self.assertIn("OrderedDict([('a0', '$\\\\pi R$')", r)

    def test_qcm_ml(self):
        test = ml_french_qcm()
        for t in test:
            s = repr(t)
            self.assertStartsWith("QuestionChoice(", s)
            self.assertIn("fr", s)
        r = repr(test)
        self.assertStartsWith("ActivityGroup(_col_acts=[", r)


if __name__ == "__main__":
    unittest.main()
