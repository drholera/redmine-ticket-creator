import yaml


class EnvironmentBase(object):

    _config = []

    def __init__(self, env_name):
        with open('./config/config.yml', 'r') as stream:
            try:
                self._config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        raise Exception("Do not create instance of EnvironmentBase class!")

