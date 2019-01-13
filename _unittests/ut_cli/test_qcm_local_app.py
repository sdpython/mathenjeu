"""
@brief      test tree node (time=2s)
"""


import sys
import os
import unittest
from io import StringIO

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

from src.mathenjeu.__main__ import main


class TempBuffer:
    "simple buffer"

    def __init__(self):
        "constructor"
        self.buffer = StringIO()

    def fprint(self, *args, **kwargs):  # pylint: disable=W0613
        "print function"
        mes = " ".join(str(_) for _ in args)
        self.buffer.write(mes)
        self.buffer.write("\n")

    def __str__(self):
        "usual"
        return self.buffer.getvalue()


class TestQcmLocalAppCli(unittest.TestCase):

    def test_src_import(self):
        """for pylint"""
        self.assertTrue(src is not None)

    def test_local_app(self):
        st = TempBuffer()
        main(args=[], fLOG=st.fprint)
        res = str(st)
        self.assertIn("python -m mathenjeu <command>", res)
        self.assertIn("Creates a local web-application", res)

    def test_local_webapp(self):
        st = TempBuffer()
        main(args=['qcm_local', '--help'], fLOG=st.fprint)
        res = str(st)
        self.assertIn("Creates a local web-application", res)

    def test_local_webapp_start(self):
        st = TempBuffer()
        main(args=['qcm_local', '-c', 'dummypwd', '-po', '8889',
                   '-u', 'abc'], fLOG=st.fprint)
        res = str(st)
        self.assertIn(
            "[create_qcm_local_app] games={'simple_french_qcm': ('simple_french_qcm', '0'), 'ml_french_qcm': ('ml_french_qcm', '0')}", res)


if __name__ == "__main__":
    unittest.main()
