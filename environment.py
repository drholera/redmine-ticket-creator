import sys
import yaml
import requests
from requests.exceptions import HTTPError
from termcolor import colored
from distutils.util import strtobool
from datetime import date


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
            full_url = self._url + 'issues.' + self._config['api_format'] + '?assigned_to_id=' + str(self._config['deployment_groups'][self._instance])
            res = requests.get(full_url, headers=self._headers)

            # Prints list of tickets which will be added to a deployment.
            self._create_tickets_list(res)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ConnectionError as e:
            print(e.with_traceback) 

    def create_deployment_ticket(self):
        """ 
        Create deployment ticket in 2 cases -
        if we have anything to deploy and if user will confirm it 
        """
        if len(self._ticket_list) <= 0:
            return

        if self._prompt('Dow you want to create a ticket with this list?'):
            try:
                ticket_subject = self._config['issue_params']['subject'].format(env=self._instance, date=date.today())
                full_url = self._url + 'issues.' + self._config['api_format']
                body = {'issue': {
                    'project_id': self._config['issue_params']['project_id'],
                    'priority_id': self._config['issue_params']['priority_id'],
                    'subject': ticket_subject,
                    'description': '\n'.join(map(str, self._ticket_list))
                } }
                res = requests.post(full_url, headers=self._headers, json=body)
                if res.status_code == 200 or res.status_code == 201:
                    # todo: Add XML/Json handling
                    result = res.json()
                    print(self._url + 'issues/' + str(result['issue']['id']))
                    return


                print(res.content)
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

    def _prompt(self, query):
        sys.stdout.write("%s [y/n]: " % query)
        val = input()
        try:
            ret = strtobool(val)
        except ValueError:
            sys.stdout.write("Please answer with y/n")
            return self._prompt(query)
        return ret