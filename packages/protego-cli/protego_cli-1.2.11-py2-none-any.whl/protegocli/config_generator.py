import uuid
import json


class ConfigGenerator:
    '''Generates config file and prints information'''

    PROTEGO_ENV_VAR_NAME = "PROTEGO_FSP_CUSTOMER_ACCOUNT_ID"
    def __init__(self, aws_account_id, python_layer_arn, logger):
        self._aws_account_id = aws_account_id
        self._python_layer_arn = python_layer_arn
        self._logger = logger

    def generate(self, output_file):
        protego_config = self.get_protego_config()
        protego_config = json.dumps(protego_config, indent=2, sort_keys=True)
        self._logger.info("===============================")
        self._logger.info("Protego FSP Layer Configuration")
        self._logger.info("===============================")
        self._logger.info(protego_config)

        with open(output_file, "w") as f:
            f.write(protego_config)

    def get_protego_config(self):
        protego_config = {}
        protego_config['python_layer'] = self._python_layer_arn
        protego_config['env'] = {}
        protego_config['env'][ConfigGenerator.PROTEGO_ENV_VAR_NAME] = self._aws_account_id + \
            ':' + uuid.uuid4().hex

        return protego_config
