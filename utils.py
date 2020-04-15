import sys
import json
import xmltodict
from distutils.util import strtobool
from requests import Response


class Utils:
    """ Helper functions """

    def prompt(self, query):
        sys.stdout.write("%s [y/n]: " % query)
        val = input()
        try:
            ret = strtobool(val)
        except ValueError:
            sys.stderr.write("Unexpected input. Shutting down.")
            return self.prompt(query)
        return ret

    def parse_response(self, r: Response, format='json'):
        if format == 'json':
            return r.json()
        elif format == 'xml':
            d = xmltodict.parse(r.content, xml_attribs=False)
            j = json.dumps(d)
            return json.loads(j)
        else:
            return r.content

    def get_issues_list(self, dict, format = 'json'):
        return dict['issues'] if format == 'json' else dict['issues']['issue']