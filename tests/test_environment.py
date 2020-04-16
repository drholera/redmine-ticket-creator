import unittest
import environment
import mockfs
import yaml
from unittest.mock import patch


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.env = environment.Environment('dev')

    def test_config(self):
        self.assertTrue(len(self.env._config) > 0)


if __name__ == '__main__':
    unittest.main()
