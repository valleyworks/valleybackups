import unittest
from valleybackups.config_handler import ConfigurationHandler
import os

class ValleybackupsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_open_config_file(self):
        """Test filesystem access to configuration file"""
        config = ConfigurationHandler("test.conf")
        os.remove(os.path.join(os.path.dirname(__file__), "test.conf"))
        self.assertTrue(config)

    def test_numbers_3_4(self):
        self.assertEqual( 12, 12)

    def test_strings_a_3(self):
        self.assertEqual( 'aaa', 'aaa')

if __name__ == '__main__':
    unittest.main()
