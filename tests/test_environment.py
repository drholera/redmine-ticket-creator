import unittest
import environment
import mockfs
import yaml
from unittest.mock import patch
import requests_mock
import requests
import io
import pytest
import json
from requests.exceptions import HTTPError
import unittest.mock as mock


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
            m.register_uri(
                'GET', 'http://success_redmine_url.com/issues.json', status_code=200)
            self.env._url = 'http://success_redmine_url.com/'
            self.assertTrue(self.env.check_connection())

    def test_broken_connection(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'GET', 'http://error_redmine_url.com/issues.json', status_code=500)
            self.env._url = 'http://error_redmine_url.com/'
            self.assertFalse(self.env.check_connection())

    def test_group_ticket_list(self):
        with requests_mock.Mocker() as m:
            with open('tests/list_tickets.json') as json_file:
                test_json = json.load(json_file)
            m.register_uri('GET', 'http://group_ticket.com/issues.json?assigned_to_id=' +
                           str(self.env._config['deployment_groups'][self.env._instance]), json=test_json)

            self.env._url = 'http://group_ticket.com/'
            self.assertTrue(self.env.group_ticket_list())

    def test_catching_exceptions(self):
        with requests_mock.Mocker() as m:
            m.register_uri(
                'GET', 'http://ex_redmine_url.com/issues.json', exc=HTTPError)
            self.env._url = 'http://ex_redmine_url.com/'
            with self.assertRaises(HTTPError):
                self.env.check_connection()

    def test_create_deployment_ticket(self):
        mock_json_result = {
            "issue": {
                "id": 123,
                "project_id": 1,
                "subject": "Example",
                "priority_id": 4
            }
        }
        with requests_mock.Mocker() as m:
            m.register_uri(
                'POST', 'http://create_deployment_ticket.com/issues.json', status_code=200, json=mock_json_result)
            self.env._url = 'http://create_deployment_ticket.com/'
            self.env._ticket_list = [1, 2]
            with mock.patch('builtins.input', return_value='y'):
                self.assertTrue(self.env.create_deployment_ticket())


if __name__ == '__main__':
    unittest.main()
