"""
@brief      test tree node (time=2s)
"""
import unittest
from pyquickhelper.loghelper import BufferedPrint
from mathenjeu.__main__ import main


class TestStaticLocalAppCli(unittest.TestCase):

    def test_local_app(self):
        st = BufferedPrint()
        main(args=[], fLOG=st.fprint)
        res = str(st)
        self.assertIn("python -m mathenjeu <command>", res)
        self.assertIn("Creates a local web-application", res)

    def test_local_webapp(self):
        st = BufferedPrint()
        main(args=['static_local', '--help'], fLOG=st.fprint)
        res = str(st)
        self.assertIn("Creates a local web-application", res)

    def test_local_webapp_start(self):
        st = BufferedPrint()
        main(args=['static_local', '-c', 'dummypwd', '-po', '8889',
                   '-u', 'abc'], fLOG=st.fprint)
        res = str(st)
        self.assertIn(
            "[create_static_local_app] create", res)


if __name__ == "__main__":
    unittest.main()
