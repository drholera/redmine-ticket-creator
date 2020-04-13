import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from utils import Utils

def test_get_issues_list():
    utils = Utils()
    json_list = {'issues': [1, 2]}
    xml_list = {'issues': {'issue': [1, 2]}}

    assert utils.get_issues_list(json_list, 'json') == [1, 2]
    assert utils.get_issues_list(json_list)
    assert utils.get_issues_list(xml_list, 'xml') == [1, 2]