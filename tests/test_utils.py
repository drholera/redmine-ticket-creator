import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import unittest.mock as mock
from utils import Utils

def test_get_issues_list():
    u = Utils()
    json_list = {'issues': [1, 2]}
    xml_list = {'issues': {'issue': [1, 2]}}

    assert u.get_issues_list(json_list, 'json') == [1, 2]
    assert u.get_issues_list(json_list) == [1, 2]
    assert u.get_issues_list(xml_list, 'xml') == [1, 2]

def test_prompt(capsys):
    u = Utils()

    with mock.patch('builtins.input', return_value = 'y'):
        assert u.prompt("Positive?") == True
        captured = capsys.readouterr()
        assert captured.out == 'Positive? [y/n]: '

    with mock.patch('builtins.input', return_value = 'yes'):
        assert u.prompt("Full yes input") == True

    # Clear stdout before next assert.
    captured = capsys.readouterr()
    with mock.patch('builtins.input', return_value = 'asdasd'):
        assert u.prompt("Random input") == False
        captured = capsys.readouterr()
        assert captured.err == 'Unexpected input. Shutting down.'

    with mock.patch('builtins.input', return_value = 'n'):
        assert u.prompt("Negative?") == False

    with mock.patch('builtins.input', return_value = 'not'):
        assert u.prompt("Negative full?") == False