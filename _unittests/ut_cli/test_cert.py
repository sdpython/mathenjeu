"""
@brief      test tree node (time=2s)
"""


import sys
import os
import unittest
from io import StringIO
from pyquickhelper.pycode import get_temp_folder, ExtTestCase

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


class TestCertCli(ExtTestCase):

    def test_src_import(self):
        """for pylint"""
        self.assertTrue(src is not None)

    def test_cert(self):
        st = TempBuffer()
        main(args=['create_self_signed_cert', '--help'], fLOG=st.fprint)
        res = str(st)
        self.assertIn("Creates a signed certificate", res)

    def test_cert_run(self):
        temp = get_temp_folder(__file__, "temp_cert")
        key_file = os.path.join(temp, "key.pem")
        cert_file = os.path.join(temp, "cert.pem")
        st = TempBuffer()
        main(args=['create_self_signed_cert', '--key_file=' +
                   key_file, '--cert_file=' + cert_file], fLOG=st.fprint)
        res = str(st)
        self.assertIn("[create_self_signed_cert] create", res)
        self.assertIn("key.pem", res)
        self.assertExists(key_file)
        self.assertExists(cert_file)


if __name__ == "__main__":
    unittest.main()
