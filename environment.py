import yaml
import requests
from requests.exceptions import HTTPError
from termcolor import colored


class Environment(object):
    """ Environment implementation. One for all """
    _config = []
    
    _instance = ''

    def __init__(self, env):
        self._instance = env
        self._init_config()


    def check_connection(self):
        """ Checking connection - retreiving list of tickets """
        try:
            url = str(self._config['redmine_settings']['url'])
            headers = {'X-Redmine-API-Key': str(self._config['redmine_settings']['api_key'])}

            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                print(colored('Connection is: 200. OK.', 'green'))
                return True
            
            print(colored('Connection is: ' + r.status_code + '. KO', 'red'))
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except ConnectionError as e:
            print(e.with_traceback)

        # If we don't have a positive result - return False.
        return False

    def _init_config(self):
        """ Load configuration """
        with open('./config/config.yml', 'r') as stream:
            try:
                self._config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)        
