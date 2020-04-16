import unittest
import environment
import mockfs
import yaml
from unittest.mock import patch
import requests_mock
import requests
import io
import pytest


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.env = environment.Environment('dev')

    @pytest.fixture(autouse=True)
    def capfd(self, capsys):
        self.capsys = capsys

    def test_config(self):
        self.assertTrue(len(self.env._config) > 0)


if __name__ == '__main__':
    unittest.main()
