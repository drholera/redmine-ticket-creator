import sys
from distutils.util import strtobool
from xml.etree import ElementTree
from requests import Response


class Utils:
    """ Helper functions """

    def prompt(self, query):
        sys.stdout.write("%s [y/n]: " % query)
        val = input()
        try:
            ret = strtobool(val)
        except ValueError:
            sys.stdout.write("Please answer with y/n")
            return self.prompt(query)
        return ret

    def parse_response(self, r: Response, format='json'):
        if format == 'json':
            return r.json()
        elif format == 'xml':
            return ElementTree.fromstring(r.content)
        else:
            return r.content
