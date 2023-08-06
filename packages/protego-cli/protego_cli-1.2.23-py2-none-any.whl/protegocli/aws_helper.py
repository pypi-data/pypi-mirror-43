import boto3
from botocore.exceptions import ClientError, ProfileNotFound
from arn import ArnLambda
from config_generator import ConfigGenerator
from protego_config import ProtegoConfig

class AWSHelper:
    def __init__(self, aws_profile, logger):
        self._logger = logger

        session_args = {}
        if aws_profile is not None:
            self._logger.debug('Using profile: ' + str(aws_profile))
            session_args["profile_name"] = aws_profile
        else:
            pass
            # self._logger.debug('No AWS profile from user')

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
        if "python" not in function_config["Runtime"].lower() and "nodejs8.10" not in function_config["Runtime"].lower():
            self._logger.error_and_exit("Invalid function runtime " + str(function_config["Runtime"]) + ". Supported runtimes are: [python2.7, python3.6, python3.7, nodejs8.10] ")

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

        runtime_name = ProtegoConfig.get_runtime_name(function_config.get("Runtime"))

        # add the needed environment variable
        environment = function_config.get("Environment", {})
        for k in protego_config.get("env", {}):
            # we need to append protego if the node env var already exists
            if k == ConfigGenerator.NODE_OPTIONS_ENV_VAR_NAME:
                if "nodejs" not in runtime_name:
                    continue
                # if the function has the node option env var
                if k in environment.get("Variables", {}):
                    # if protego is already in that var
                    if ConfigGenerator.NODE_OPTIONS_ENV_VAR_VALUE in environment["Variables"][k]:
                        self._logger.debug("Function already has protego NODE_OPTIONS environment variable")
                        continue
                    else:
                        self._logger.debug("Append protego NODE_OPTIONS to function environment variable")
                        # append protego to the current value
                        value = ConfigGenerator.NODE_OPTIONS_ENV_VAR_VALUE + " " + environment["Variables"][k]
                else:
                    value =  ConfigGenerator.NODE_OPTIONS_ENV_VAR_VALUE
            else:
                value = protego_config["env"][k]

            environment.setdefault("Variables", {})[k] = value

        layers = [l["Arn"] for l in function_config.get("Layers", [])]
        # removes any other protego fsp layer from this function
        layers = filter(lambda l: "protego-fsp-" not in l, layers)

        # adds the needed layer
        runtime_key = str(runtime_name) + "-layer"

        if runtime_key not in protego_config:
            self._logger.error_and_exit("Failed to find layer for runtime: " + str(runtime_name))

        if arn.region not in protego_config[runtime_key]:
            self._logger.error_and_exit("Failed to find "+str(runtime_name)+" layer for region " + arn.region)

        layers.append(protego_config[runtime_key][arn.region])

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

        runtime_name = ProtegoConfig.get_runtime_name(function_config.get("Runtime"))

        update_config = {}

        # remove the needed environment variables
        environment = function_config.get("Environment", {})

        k = ConfigGenerator.PROTEGO_ENV_VAR_NAME
        if k in environment.get("Variables", {}):
            del environment["Variables"][k]
            update_config["Environment"] = environment

        if remove_layer:
            if "nodejs" in runtime_name:
                k = ConfigGenerator.NODE_OPTIONS_ENV_VAR_NAME
                if k in environment.get("Variables", {}):
                    new_value = environment["Variables"][k].replace(ConfigGenerator.NODE_OPTIONS_ENV_VAR_VALUE, "").strip()
                    if new_value:
                        self._logger.debug("Remove only protego from NODE_OPTIONS environment variable")
                        environment["Variables"][k] = new_value
                    else:
                        del environment["Variables"][k]

                    update_config["Environment"] = environment

            layers = [l["Arn"] for l in function_config.get("Layers", [])]
            # removes any protego fsp layer from this function
            layers_without_protego = filter(lambda l: "protego-fsp-" not in l, layers)
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
