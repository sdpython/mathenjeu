"""
@brief      test log(time=1s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from mathenjeu.activities import Display
from mathenjeu.tests import simple_french_qcm, simple_cinema_qcm


class TestRepr(ExtTestCase):

    def test_repr(self):
        disp = Display(1, 'eid1')
        r = repr(disp)
        self.assertEqual(r, "Display(_col_eid=1, _col_name='eid1')")

    def test_french_qcm(self):
        test = simple_french_qcm()
        for t in test:
            s = repr(t)
            self.assertStartsWith("QuestionChoice(", s)
            self.assertIn("fr", s)
        r = repr(test)
        self.assertStartsWith("ActivityGroup(_col_acts=[", r)
        self.assertIn("OrderedDict([('a0', '$\\\\pi R$')", r)

    def test_cinema_qcm(self):
        test = simple_cinema_qcm()
        for t in test:
            s = repr(t)
            self.assertStartsWith("QuestionChoice(", s)
            self.assertIn("fr", s)
        r = repr(test)
        self.assertStartsWith("ActivityGroup(_col_acts=[", r)
        self.assertIn("OrderedDict([(", r)

    def test_expected(self):
        test = simple_cinema_qcm()
        for qu in test:
            r = qu.ExpectedAnswers
            self.assertIsInstance(r, list)
            self.assertEqual(len(r), 1)
            self.assertEqual(r[0][0], 'a')
        exp = test.expected_answers()
        self.assertIn(['simple_cinema_qcm-0-a0'], exp)


if __name__ == "__main__":
    unittest.main()
