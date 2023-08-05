import os
import sys
import yaml


class ProtegoConfig:
    PROTEGO_CONFIG_FOLDER = '.protego'
    PROTEGO_CONFIG_FILE_NAME = 'protego.yml'
    PROTEGO_ACCOUNT_ID_NAME = 'protegoAccountId'
    PROTEGO_TOKEN_NAME = 'protegoAccessToken'

    def __init__(self, protego_account_id, protego_token, logger):
        self._protego_account_id = protego_account_id
        self._protego_token = protego_token
        self._logger = logger
        self.__parse_protego_config()

    def protego_account_id(self):
        return self._protego_account_id

    def protego_token(self):
        return self._protego_token

    def __get_protego_config(self):
        config_file = os.path.join(
            os.getcwd(), ProtegoConfig.PROTEGO_CONFIG_FILE_NAME)

        if os.path.isfile(config_file):
            self._logger.debug('Reading token from: ' + str(config_file))
            return config_file

        user_home = os.path.expanduser('~')
        config_file = os.path.join(
            user_home, ProtegoConfig.PROTEGO_CONFIG_FOLDER, ProtegoConfig.PROTEGO_CONFIG_FILE_NAME)
        if os.path.isfile(config_file):
            self._logger.debug('Reading token from: ' + str(config_file))
            return config_file

        self._logger.error('Failed to find ' +
                           ProtegoConfig.PROTEGO_CONFIG_FILE_NAME)
        self._logger.error_and_exit(
            'protego_account_id and protego_token must be provided')

        return None

    def __parse_protego_config(self):
        if self._protego_account_id is not None and self._protego_token is not None:
            self._logger.debug('Using token passed from command line')
            return

        config_file = self.__get_protego_config()
        with open(config_file, 'r') as config_stream:
            try:
                yaml_config = yaml.load(config_stream)

                if self._protego_account_id is None:
                    self._protego_account_id = yaml_config.get(
                        ProtegoConfig.PROTEGO_ACCOUNT_ID_NAME, None)
                    self._logger.debug(
                        'from yml protegoAccountId: ' + str(self._protego_account_id))

                if self._protego_token is None:
                    self._protego_token = yaml_config.get(
                        ProtegoConfig.PROTEGO_TOKEN_NAME, None)
                    self._logger.debug(
                        'from yml protegoAccessToken: ' + str(self._protego_token))

                if self._protego_account_id is None or self._protego_token is None:
                    self._logger.error_and_exit('Failed to read protego tokens')


            except yaml.YAMLError as err:
                self._logger.error('Failed to parse ' +
                                   ProtegoConfig.PROTEGO_CONFIG_FILE_NAME)
                self._logger.error_and_exit(str(err))
