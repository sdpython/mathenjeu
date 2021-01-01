"""
@brief      test tree node (time=2s)
"""
import os
import unittest
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from pyquickhelper.loghelper import BufferedPrint
from mathenjeu.__main__ import main


class TestQcmHttpsAppCli(ExtTestCase):

    def test_https_webapp(self):
        st = BufferedPrint()
        main(args=['qcm_https', '--help'], fLOG=st.fprint)
        res = str(st)
        self.assertIn("usage: qcm_https", res)

    def test_https_webapp_start(self):
        temp = get_temp_folder(__file__, "temp_qcm_https")
        st = BufferedPrint()
        key_file = os.path.join(temp, "key.pem")
        cert_file = os.path.join(temp, "cert.pem")
        main(args=['create_self_signed_cert', '--keyfile=' +
                   key_file, '--certfile=' + cert_file], fLOG=st.fprint)
        main(args=['qcm_https', '--cookie_key=dummypwd', '--port=8889',
                   '--userpwd=abc', '--ca_certs="{0}"'.format(temp),
                   '--keyfile=key.pem', '--certfile=cert.pem',
                   '--folder=' + temp],
             fLOG=st.fprint)
        res = str(st)
        self.assertIn('[create_self_signed_cert]', res)
        self.assertIn('[create_qcm_https_app] saved file', res)
        self.assertIn('apphyper.py', res)


if __name__ == "__main__":
    unittest.main()
