import logging
import unittest

import os

import shutil

from doxygen import Generator


class DoxygenGeneratorTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DoxygenGeneratorTest, self).__init__(*args, **kwargs)
        logging.disable(logging.CRITICAL)
        self.doxyfile_original = os.path.join(os.path.dirname(__file__), "assets/Doxyfile")
        self.path_to_clean = []

    def setUp(self):
        self.path_to_clean = []

    def tearDown(self):
        for file in self.path_to_clean:
            if file is not None and os.path.exists(file):
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    shutil.rmtree(file)

    def test_build_not_existing_configuration(self):
        self.assertRaises(FileNotFoundError, Generator, "./NotExisting/file/Doxyfile")

    def test_build_without_compress(self):
        doxy_builder = Generator(self.doxyfile_original)
        output_folder_path = doxy_builder.build()

        self.assertIsNotNone(output_folder_path)
        self.path_to_clean.append(output_folder_path)
        self.assertTrue(os.path.isdir(output_folder_path))
        self.assertIsNotNone(os.listdir(output_folder_path))

    def test_build_with_compress(self):
        doxy_builder = Generator(self.doxyfile_original)
        output_zip_archive = doxy_builder.build(clean=True, generate_zip=True)

        self.assertIsNotNone(output_zip_archive)
        self.path_to_clean.append(output_zip_archive)
        self.assertTrue(os.path.isfile(output_zip_archive))

if __name__ == '__main__':
    unittest.main()
