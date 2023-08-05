import boto3
from botocore.exceptions import ClientError, ProfileNotFound
from arn import ArnLambda
from config_generator import ConfigGenerator

class AWSHelper:
    def __init__(self, aws_profile, logger):
        self._logger = logger

        session_args = {}
        if aws_profile is not None:
            self._logger.debug('Using profile: ' + str(aws_profile))
            session_args["profile_name"] = aws_profile
        else:
            self._logger.debug('Using default profile')

        try:
            self.boto3_session = boto3.Session(**session_args)
        except ProfileNotFound as e:
            self._logger.error_and_exit(str(e))

    def get_account_id(self):
        sts_client = self.boto3_session.client('sts')
        account_id = sts_client.get_caller_identity().get('Account')
        self._logger.debug('AWS Account Id: ' + str(account_id))
        return account_id

    def __get_function_config(self, lambda_client, function_name):
        self._logger.debug("Get the function: " + function_name)
        try:
            # get the current function configuration
            function_config = lambda_client.get_function_configuration(
                FunctionName=function_name)
        except ClientError as e:
            self._logger.error_and_exit("Failed to get function: " + function_name +". Try to check your aws-profile or region.\n" + str(e))

        # validate that it's a python function
        if "python" not in function_config["Runtime"].lower():
            self._logger.error_and_exit("Invalid function runtime " + str(function_config["Runtime"]) + ". Function must have python runtime. ")

        return function_config

    def __update_function_config(self, lambda_client, function_name, config):
        if len(config) == 0:
            self._logger.info("No need to update function ("+function_name+") configuration")
            return

        self._logger.debug("Update config for function: " + function_name)

        try:
            # get the current function configuration
            lambda_client.update_function_configuration(
                FunctionName=function_name,
                **config)
        # except ClientError as e:
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDeniedException':
                self._logger.error_and_exit("Failed to update function configuration. Account has No permission to read layer.\n" + str(e))
            self._logger.error_and_exit("Failed to update function: " + function_name + "; " + str(e))



    def add_config_to_function(self, function_arn, protego_config):
        arn = ArnLambda(function_arn)

        # init a client in the right region
        lambda_client = self.boto3_session.client("lambda", region_name=arn.region)

        # get the current function configuration
        function_config = self.__get_function_config(lambda_client, arn.function_name)

        # add the needed environment variable
        environment = function_config.get("Environment", {})
        for k in protego_config.get("env", {}):
            environment.setdefault("Variables", {})[k] = protego_config["env"][k]

        layers = [l["Arn"] for l in function_config.get("Layers", [])]
        # removes any other protego fsp layer from this function
        layers = filter(lambda l: "protego-fsp-python-layer" not in l, layers)

        # adds the needed layer
        layers.append(protego_config["python_layer"])

        self.__update_function_config(lambda_client,
                                      arn.function_name,
                                      {"Environment": environment, "Layers": layers})

        self._logger.info("Successfully Added Protego Fsp Layer")


    def remove_config_for_function(self, function_arn, remove_layer=False):
        arn = ArnLambda(function_arn)

        # init a client in the right region
        lambda_client = self.boto3_session.client("lambda", region_name=arn.region)

        # get the current function configuration
        function_config = self.__get_function_config(lambda_client, arn.function_name)

        update_config = {}

        # remove the needed environment variable
        environment = function_config.get("Environment", {})
        k = ConfigGenerator.PROTEGO_ENV_VAR_NAME
        if k in environment.get("Variables", {}):
            del environment["Variables"][k]
            update_config["Environment"] = environment

        # self._logger.info("Successfully Reset Protego Fsp")

        if remove_layer:
            layers = [l["Arn"] for l in function_config.get("Layers", [])]
            # removes any protego fsp layer from this function
            layers_without_protego = filter(lambda l: "protego-fsp-python-layer" not in l, layers)
            # check if we need to update the function layers
            if layers != layers_without_protego:
                update_config["Layers"] = layers_without_protego


        self.__update_function_config(lambda_client,
                                      arn.function_name,
                                      update_config)
        if remove_layer:
            self._logger.info("Successfully removed Protego Fsp Layer")
        else:
            self._logger.info("Successfully reset Protego Fsp Layer")
