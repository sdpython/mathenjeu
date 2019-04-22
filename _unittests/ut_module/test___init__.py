"""
@brief      test log(time=0s)
"""
import unittest
from pyquickhelper.loghelper import fLOG
from mathenjeu import check, _setup_hook


class TestInit(unittest.TestCase):

    def test_check(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        assert check()
        _setup_hook()


if __name__ == "__main__":
    unittest.main()
