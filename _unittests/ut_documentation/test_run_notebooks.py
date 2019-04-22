# -*- coding: utf-8 -*-
"""
@brief      test log(time=21s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.ipythonhelper import test_notebook_execution_coverage
import jyquickhelper
import mathenjeu


class TestRunNotebooksPython(unittest.TestCase):

    def setUp(self):
        "module to import before executing a notebook"
        self.assertTrue(jyquickhelper is not None)

    def test_notebook_donnees_anonymisees(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(mathenjeu is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks")
        test_notebook_execution_coverage(__file__, "donnees_anonymisees", folder, 'mathenjeu',
                                         copy_files=["logs/qcm100.txt"], fLOG=fLOG)

    def test_notebook_example_logs(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        self.assertTrue(mathenjeu is not None)
        self.assertTrue(jyquickhelper is not None)
        folder = os.path.join(os.path.dirname(__file__),
                              "..", "..", "_doc", "notebooks")
        test_notebook_execution_coverage(__file__, "example_logs", folder, 'mathenjeu',
                                         copy_files=["logs/QCMApp.log"], fLOG=fLOG)


if __name__ == "__main__":
    unittest.main()
