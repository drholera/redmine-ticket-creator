import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import unittest.mock as mock
from utils import Utils

def test_get_issues_list():
    utils = Utils()
    json_list = {'issues': [1, 2]}
    xml_list = {'issues': {'issue': [1, 2]}}

    assert utils.get_issues_list(json_list, 'json') == [1, 2]
    assert utils.get_issues_list(json_list) == [1, 2]
    assert utils.get_issues_list(xml_list, 'xml') == [1, 2]

def test_prompt(capsys):
    utils = Utils()

    with mock.patch('builtins.input', return_value = 'y'):
        assert utils.prompt("Positive?") == True

    with mock.patch('builtins.input', return_value = 'yes'):
        assert utils.prompt("Full yes input") == True

    # Clear stdout before next assert.
    captured = capsys.readouterr()
    with mock.patch('builtins.input', return_value = 'asdasd'):
        assert utils.prompt("Random input") == False
        captured = capsys.readouterr()
        assert captured.err == 'Unexpected input. Shutting down.'

    with mock.patch('builtins.input', return_value = 'n'):
        assert utils.prompt("Negative?") == False

    with mock.patch('builtins.input', return_value = 'not'):
        assert utils.prompt("Negative full?") == False