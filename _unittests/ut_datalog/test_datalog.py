"""
@brief      test tree node (time=2s)
"""


import sys
import os
import unittest
import datetime
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

from src.mathenjeu.datalog import enumerate_qcmlog


class TestLocalAppCli(ExtTestCase):

    def test_src_import(self):
        """for pylint"""
        self.assertTrue(src is not None)

    def test_datadf(self):
        this = os.path.abspath(os.path.dirname(__file__))
        logs = [os.path.join(this, "data", "QCMApp.log")]
        obs = list(enumerate_qcmlog(logs))
        self.assertEqual(obs[0], {'alias': 'xavierd', 'time': datetime.datetime(
            2018, 12, 12, 17, 56, 29, 989000), 'qtime': 'begin'})
        self.assertEqual(obs[-1], {'alias': 'xavierg', 'time': datetime.datetime(2018, 12, 12, 23, 10, 37, 527000), 'qtime': 'end',
                                   'simple_french_qcm-8-ANS': ' ', 'simple_french_qcm-8-b': 'ok',
                                   'game': 'simple_french_qcm', 'qn': '8', 'next': 'None', 'simple_french_qcm-8-nbvisit': 1.0,
                                   'simple_french_qcm-8-duration': datetime.timedelta(seconds=1, microseconds=422000)})


if __name__ == "__main__":
    unittest.main()
