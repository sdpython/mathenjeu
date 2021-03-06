"""
@brief      test tree node (time=2s)
"""
import os
import unittest
import datetime
import pandas
from pyquickhelper.pycode import ExtTestCase
from mathenjeu.datalog import enumerate_qcmlog, enumerate_qcmlogdf


class TestLocalAppData(ExtTestCase):

    def test_datalog(self):
        this = os.path.abspath(os.path.dirname(__file__))
        logs = [os.path.join(this, "data", "QCMApp.log")]
        obs = list(enumerate_qcmlog(logs))
        exp = {'person_id': 'c241c15008614ea67480', 'alias': 'xavierd',
               'time': datetime.datetime(2018, 12, 12, 17, 56, 29, 989000),
               'qtime': 'begin'}
        self.assertEqual(obs[0], exp)
        exp = {'person_id': '8a8c40ad28eb1206efd5',
               'alias': 'xavierg',
               'time': datetime.datetime(2018, 12, 12, 23, 10, 37, 527000),
               'qtime': 'end',
               'simple_french_qcm-8-ANS': ' ',
               'simple_french_qcm-8-b': 'ok',
               'game': 'simple_french_qcm',
               'qn': '8',
               'next': 'None',
               'simple_french_qcm-8-nbvisit': 1.0,
               'simple_french_qcm-8-good': 0,
               'simple_french_qcm-8-duration': datetime.timedelta(seconds=1, microseconds=422000)}
        self.assertEqual(obs[-1], exp)

    def test_datalog_df(self):
        this = os.path.abspath(os.path.dirname(__file__))
        logs = [os.path.join(this, "data", "QCMApp.log")]
        dfs = list(enumerate_qcmlogdf(logs))
        self.assertEqual(len(dfs), 5)
        merged = pandas.concat(dfs, sort=False)
        self.assertEqual(merged.shape[0], 5)
        self.assertEqual(merged.shape[1], 58)
        values = list(merged["simple_french_qcm-8-ANS"])
        self.assertIn(" Prout", values)
        # print(merged.T)


if __name__ == "__main__":
    unittest.main()
