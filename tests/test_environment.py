import unittest
import environment
import mockfs
import yaml
from unittest.mock import patch
import requests_mock
import requests
import io
import pytest
from requests.exceptions import HTTPError


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.env = environment.Environment('dev')

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def test_config(self):
        self.assertTrue(len(self.env._config) > 0)

    def test_ok_connection(self):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'http://success_redmine_url.com/issues.json', status_code=200)
            self.env._url = 'http://success_redmine_url.com/'
            self.assertTrue(self.env.check_connection())

    def test_broken_connection(self):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'http://error_redmine_url.com/issues.json', status_code=500)
            self.env._url = 'http://error_redmine_url.com/'
            self.assertFalse(self.env.check_connection())

    def test_catching_exceptions(self):
        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'http://ex_redmine_url.com/issues.json', exc=HTTPError)
            self.env._url = 'http://ex_redmine_url.com/'
            self.assertRaises(HTTPError, self.env.check_connection())
                


if __name__ == '__main__':
    unittest.main()
