import logging
import unittest

import os

from doxygen.configParser import ConfigParser


class DoxygenConfigParserTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DoxygenConfigParserTest, self).__init__(*args, **kwargs)
        self.doxyfile_original = os.path.join(os.path.dirname(__file__), "assets/Doxyfile")
        self.doxyfile_working = "./Doxyfile.tmp"

    def test_try_use_not_existing_doxyfile(self):
        config_parser = ConfigParser()
        self.assertRaises(FileNotFoundError, config_parser.load_configuration, "./NotExisting/file/Doxyfile")

    def tearDown(self):
        if os.path.exists(self.doxyfile_working):
            os.remove(self.doxyfile_working)

    def test_load_configuration(self):
        config_parser = ConfigParser()
        configuration = config_parser.load_configuration(self.doxyfile_original)
        self.assertIsInstance(configuration, dict)
        self.assertEqual(len(configuration), 270)

    def test_update_configuration(self):
        config_parser = ConfigParser()

        configuration = config_parser.load_configuration(self.doxyfile_original)
        self.assertTrue('PROJECT_NAME' in configuration)
        self.assertTrue('PROJECT_NUMBER' in configuration)
        self.assertTrue('FILE_PATTERNS' in configuration)

        configuration['PROJECT_NAME'] = 'something cool'
        configuration['PROJECT_NUMBER'] = '1.2.3.4'
        configuration['FILE_PATTERNS'].append("*.dtc")

        config_parser.store_configuration(configuration, self.doxyfile_working)

        configuration_updated = config_parser.load_configuration(self.doxyfile_working)
        self.assertTrue('PROJECT_NAME' in configuration_updated)
        self.assertTrue('PROJECT_NUMBER' in configuration_updated)
        self.assertTrue('FILE_PATTERNS' in configuration_updated)

        self.assertEqual(configuration_updated['PROJECT_NAME'], 'something cool')
        self.assertEqual(configuration_updated['PROJECT_NUMBER'], '1.2.3.4')
        self.assertTrue("*.dtc" in configuration_updated['FILE_PATTERNS'])


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)
    unittest.main()
