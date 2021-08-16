#!/usr/bin/python
import subprocess
from httpfs.tests.test_helpers import testfiles_dir, runUploadTest
from httpfs.common import build_confs_from_json
import unittest

FSCONFS = build_confs_from_json()

## IP & port for a mock up http server, for simulation of a remote web iamge server.
MOCKSRV_PORT = '9998'
MOCKSRV_IP = '127.0.0.1' # loopback address by default
MOCKSRV = f'http://{MOCKSRV_IP}:{MOCKSRV_PORT}'

class HttpFsUnitTests(unittest.TestCase):

    def test_01(self):
        testName = "Unknown fsroot, Upload 1 Local Image"
        md = ''
        ts = [str(testfiles_dir/'white.png')]

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_02(self):
        testName = "Unknown fsroot, Upload 2 Local Images"
        md = ''
        ts = [str(testfiles_dir/'white.png'), str(testfiles_dir/'white.png')]

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)


    def test_03(self):
        testName = "Unknown fsroot, Upload Same Local Image Twice"
        md = ''
        ts = [str(testfiles_dir/'white.png'), str(testfiles_dir/'white.png')]

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_04(self):
        testName = "Unknown fsroot, Upload 1 Web Image URL"
        md = ''
        ts = [f'{MOCKSRV}/typora-icon.png']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_05(self):
        testName = "Unknown fsroot, Upload 2 Web Image URLs"
        md = ''
        ts = [f'{MOCKSRV}/typora-icon.png', f'{MOCKSRV}/typora-icon2.png']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_06(self):
        testName = "Unknown fsroot, Upload Same Web Image URL Twice (atm, return code 1 (stderr) expected for SUCCESS)"
        md = ''
        ts = [f'{MOCKSRV}/typora-icon.png', f'{MOCKSRV}/typora-icon.png']

        code = runUploadTest(testName, md, ts, printResult=False)
        # this tests returning for STDERR code (1), because uploader script will download the same URL under single temporary name, while the single temporary file will be removed immediately after the first upload, with no second one to be found for upload.
        print('[RESULT]:')
        if code == 0:
            print('NOT Expected behaviour.')
        elif code == 1:
            print('SUCCESS')
        self.assertTrue(code == 1)

    def test_07(self):
        testName = "Unknown fsroot, Upload 3 Web Image URLs"
        md = ''
        ts = [f'{MOCKSRV}/typora-icon.png', f'{MOCKSRV}/typora-icon2.png', f'{MOCKSRV}/blue.gif']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_08(self):
        testName = "Managed fsroot, Upload 3 Web Image URLs"
        md = str(FSCONFS['default'].fsroot / 'dummpy.md')
        ts = [f'{MOCKSRV}/typora-icon.png', f'{MOCKSRV}/typora-icon2.png', f'{MOCKSRV}/blue.gif']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_09(self):
        testName = "Upload Web Image URLS of Various Format (png,jpg,gif,svg,eps)"
        md = str(FSCONFS['default'].fsroot / 'dummpy.md')
        ts = [f'{MOCKSRV}/white.png', f'{MOCKSRV}/red.jpg', f'{MOCKSRV}/blue.gif', f'{MOCKSRV}/pink.svg', f'{MOCKSRV}/yellow.eps']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_10(self):
        testName = "Upload Image URLs including URL encoded chars (%20, %2B)"
        md = str(FSCONFS['default'].fsroot / 'dummpy.md')
        ts = [f'{MOCKSRV}/red%20square.jpg', f'{MOCKSRV}/red%2Bsquare.jpg']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)


    def test_11(self):
        testName = "Upload Image URLs including URL encoded chars of 'encoded' chars (((ie. URL(%20) == %2520, URL(%2B) == %252B)"
        md = str(FSCONFS['default'].fsroot / 'dummpy.md')
        ts = [f'{MOCKSRV}/red%2520square.jpg', f'{MOCKSRV}/red%252Bsquare.jpg']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

    def test_12(self):
        testName = "Upload Local Non-Images of Various File Format (txt,md,odt,pdf)"
        md = str(FSCONFS['default'].fsroot / 'dummpy.md')
        ts = [f'{MOCKSRV}/sample.txt', f'{MOCKSRV}/sample.md', f'{MOCKSRV}/sample.odt', f'{MOCKSRV}/sample.pdf']

        code = runUploadTest(testName, md, ts)
        self.assertTrue(code == 0)

if __name__ == '__main__':

    """
    Please run while httpfs-server is running
    The unittests here are not exhaustive, but covers very basic sanity.
    """

    try:
        ## simple http server to mock a remote server. for unit testing purpose.
        httpServerProcess = subprocess.Popen(['python', '-m', 'http.server', MOCKSRV_PORT, '--bind', MOCKSRV_IP, '--directory', f'{str(testfiles_dir)}'])

        # start unit test
        unittest.main()

    except Exception as e:
        print(e)
    finally:
        # dont forget to terminate process regardless of success or failure
        httpServerProcess.terminate()

