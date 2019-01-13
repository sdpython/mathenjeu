# -*- coding: utf-8 -*-
"""
@brief      test log(time=21s)
"""

import sys
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import jyquickhelper


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

import src.mathenjeu


class TestRunNotebooksPython(unittest.TestCase):

    def setUp(self):
        "module to import before executing a notebook"
        self.assertTrue(jyquickhelper is not None)

    def test_notebook_donnees_anonymisees(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(src.mathenjeu is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks")
        test_notebook_execution_coverage(__file__, "donnees_anonymisees", folder, 'mathenjeu',
                                         copy_files=["logs/qcm100.txt"], fLOG=fLOG)

    def test_notebook_example_logs(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(src.mathenjeu is not None)
        self.assertTrue(jyquickhelper is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks")
        test_notebook_execution_coverage(__file__, "example_logs", folder, 'mathenjeu',
                                         copy_files=["logs/QCMApp.log"], fLOG=fLOG)


if __name__ == "__main__":
    unittest.main()
