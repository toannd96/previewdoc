import unittest
import os
import shutil
import tempfile
import datetime
from config import BaseConfig
from resources.upload import _mkdir_upload_folder, allowed_file, convert_file


class TestFolderMkdir(unittest.TestCase):
    def setUp(self):
        self.path = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_mkdir_upload_folder(self):
        upload_path = os.path.join(
            self.path, str(datetime.date.today().strftime("%Y/%m/%d")))
        result, folder_path = _mkdir_upload_folder(upload_path)
        self.assertTrue(result)
        self.assertEqual(folder_path, upload_path)


class TestAllowedFile(unittest.TestCase):
    def test_type_file(self):
        self.assertFalse(allowed_file("test"))
        self.assertFalse(allowed_file("test.img"))
        self.assertTrue(allowed_file("test.doc"))
        self.assertTrue(allowed_file("test.DoC"))


class TestConvertFile(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def test_convert_file(self):
        file_path = os.path.join(self.tempdir, "test.txt")
        f = open(file_path, 'w')
        f.write('test create file txt and convert to pdf')
        f.close()

        f = open(file_path)
        self.assertEqual(f.read(),
                         'test create file txt and convert to pdf')  

        result, file_convert = convert_file(file_path)
        self.assertTrue(file_convert, file_path)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        shutil.rmtree(os.path.join(os.getcwd(),
                                   BaseConfig.CONVERT_FOLDER))  


if __name__ == '__main__':
    unittest.main()
