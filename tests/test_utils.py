from utils import Utils
import requests_mock
import unittest.mock as mock
import sys
import os
import requests
from xml.parsers.expat import ExpatError
from json.decoder import JSONDecodeError
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


def test_get_issues_list():
    u = Utils()
    json_list = {'issues': [1, 2]}
    xml_list = {'issues': {'issue': [1, 2]}}

    assert u.get_issues_list(json_list, 'json') == [1, 2]
    assert u.get_issues_list(json_list) == [1, 2]
    assert u.get_issues_list(xml_list, 'xml') == [1, 2]


def test_prompt(capsys):
    u = Utils()

    with mock.patch('builtins.input', return_value='y'):
        assert u.prompt("Positive?") == True
        captured = capsys.readouterr()
        assert captured.out == 'Positive? [y/n]: '

    with mock.patch('builtins.input', return_value='yes'):
        assert u.prompt("Full yes input") == True

    with mock.patch('builtins.input', return_value='n'):
        assert u.prompt("Negative?") == False

    with mock.patch('builtins.input', return_value='no'):
        assert u.prompt("Negative full?") == False


def test_parse_response():
    u = Utils()
    test_json = {
        'issue': {
            "id": "1",
            "title": "Test title"
        }
    }

    test_xml = '''<?xml version="1.0" encoding="UTF-8" ?>
                    <issue>
                        <id>1</id>
                        <title>Test title</title>
                    </issue>'''
    
    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'http://test_json.com', json=test_json)
        assert u.parse_response(requests.get('http://test_json.com')) == test_json
        assert u.parse_response(requests.get('http://test_json.com'), 'json') == test_json

        # Trying to parse Json as XML.
        try :
            u.parse_response(requests.get('http://test_json.com'), 'xml') != test_json
            assert False
        except ExpatError:
            assert True

        m.register_uri('GET', 'http://test_xml.com', text=test_xml)
        # Return dict must be the same is test_json variable.
        assert u.parse_response(requests.get('http://test_xml.com'), 'xml') == test_json

        # Trying to parse Json as XML.
        try :
            u.parse_response(requests.get('http://test_xml.com'), 'json') == test_json
            u.parse_response(requests.get('http://test_xml.com')) == test_json
            assert False
        except JSONDecodeError:
            assert True

        m.register_uri('GET', 'http://test_text.com', content=bytes('Some text', 'utf-8'))
        assert u.parse_response(requests.get('http://test_text.com'), 'text') == bytes('Some text', 'utf-8')
