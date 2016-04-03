import unittest
from valleybackups.config_handler import ConfigurationHandler
import os
import sys

class ValleybackupsTest(unittest.TestCase):

    def setUp(self):
        self.config = ConfigurationHandler("test.conf")

    def test_open_config_file(self):
        """Test filesystem access to configuration file"""
        config = ConfigurationHandler("test.conf")
        self.assertTrue(config)

    def test_set_valid_config(self):
        self.assertTrue(self.config.set_config('base', 'aws_account_id', '123123123'))

    def test_set_invalid_config(self):
        self.assertFalse(self.config.set_config('base', 'invalid_config', '123123123'))

    def tearDown(self):
        os.remove(os.path.join(os.path.dirname(__file__), "test.conf"))

if __name__ == '__main__':
    unittest.main()
