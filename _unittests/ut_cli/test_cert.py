"""
@brief      test tree node (time=2s)
"""
import os
import unittest
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from pyquickhelper.loghelper import BufferedPrint
from mathenjeu.__main__ import main


class TestCertCli(ExtTestCase):

    def test_cert(self):
        st = BufferedPrint()
        main(args=['create_self_signed_cert', '--help'], fLOG=st.fprint)
        res = str(st)
        self.assertIn("usage: create_self_signed_cert", res)

    def test_cert_run(self):
        temp = get_temp_folder(__file__, "temp_cert")
        key_file = os.path.join(temp, "key.pem")
        cert_file = os.path.join(temp, "cert.pem")
        st = BufferedPrint()
        main(args=['create_self_signed_cert', '-k',
                   key_file, '-c', cert_file], fLOG=st.fprint)
        res = str(st)
        self.assertIn("[create_self_signed_cert] create", res)
        self.assertIn("key.pem", res)
        self.assertExists(key_file)
        self.assertExists(cert_file)


if __name__ == "__main__":
    unittest.main()
