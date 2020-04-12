import yaml
import requests
from requests.exceptions import HTTPError
from termcolor import colored


class Environment(object):
    """ Environment implementation. One for all """
    _config = []
    
    _instance = None
    _url = None
    _headers = None
    _ticket_list = []

    def __init__(self, env):
        self._instance = env
        self._config = self._init_config()
        self._url = str(self._config['redmine_settings']['url'])
        self._headers = {'X-Redmine-API-Key': str(self._config['redmine_settings']['api_key'])}


    def check_connection(self):
        """ Checking connection - retreiving list of tickets """
        try:
            res = requests.get(self._url + 'issues.' + self._config['api_format'], headers=self._headers)
            if res.status_code == 200:
                print(colored('Connection is: 200. OK.', 'green'))
                return True
            
            print(colored('Connection is: ' + res.status_code + '. KO', 'red'))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ConnectionError as e:
            print(e.with_traceback)

        # If we don't have a positive result - return False.
        return False

    def group_ticket_list(self):
        try:
            full_url = self._url + 'issues.' + self._config['api_format'] + '?assigned_to_id=' + self._config['deployment_groups'][self._instance]
            res = requests.get(full_url, headers=self._headers)

            # Prints list of tickets which will be added to a deployment.
            self._create_tickets_list(res)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ConnectionError as e:
            print(e.with_traceback) 

    @staticmethod
    def get_config():
        """ Load configuration """
        with open('./config/config.yml', 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return False        

    # Protected section.
    @classmethod
    def _init_config(cls):
        """ Load configuration """
        return cls.get_config()

    def _create_tickets_list(self, r: requests.Response):
        """ Create a pretty formatter list from a redmine response """
        print(colored('Issues list:', 'yellow'))
        if self._config['api_format'] == 'json':
            result = r.json()
            for value in result['issues']:
                issue_link = self._config['redmine_settings']['url'] + 'issues/' + str(value['id'])
                issue_title = value['subject']
                self._ticket_list.append(issue_link + ' ' + issue_title)
                print(colored(issue_link + ' ' + issue_title, 'yellow', attrs=['underline']))
        else:
            # @todo: add XML parsing functionality. 
            pass