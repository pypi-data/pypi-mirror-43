import argparse

from arn import ArnLambda
from aws_helper import AWSHelper
from cli_logger import CLILogger
from config_generator import ConfigGenerator
from fsp_downloader import FSPDownloader
from manifest_reader import ManifestReader
from protego_config import ProtegoConfig


def formatter(prog):
    return argparse.RawDescriptionHelpFormatter(prog, width=120)


def get_input_arguments():
    # Args

    epilog = """
    
protego.yml file example:

    Account:
      ProtegoAccountId: <YourProtegoAccountId>
      ProtegoAccessToken: <YourProtegoAccessToken>

    """

    parser = argparse.ArgumentParser(
        description="Protego FSP Layers Info Add / Get / Remove",
        formatter_class=formatter,
        epilog=epilog
    )

    parser.add_argument("-m", "--mode", required=False, choices=['get', 'add', 'reset', 'remove'], help="Action Mode")

    # General arguments
    parser.add_argument("-p", "--protego-account-id", required=False, default=None, help="Protego Account ID")
    parser.add_argument("-t", "--protego-access-token", required=False, default=None, help="Protego Token")
    parser.add_argument("-a", "--aws-profile", required=False, default=None, help="(Optional) AWS profile")
    parser.add_argument("-s", "--fsp-version", required=False, default="latest", help="(Optional) FSP Version(default: latest)")
    parser.add_argument("-q", "--quiet", required=False, action='store_true', help="(Optional) Quiet mode: output only the json output")
    parser.add_argument("-v", "--verbose", required=False, action='store_true', help="(Optional) Verbose debug logs")

    # get fsp info
    parser.add_argument("-r", "--runtime", required=False, default=None, help="(Optional) Environment runtime[python2.7, python3.6, python3.7, nodejs6.10, nodejs8.10]")
    parser.add_argument("-R", "--region", required=False, default=None, help="(Optional) The region of which FSP layer")
    parser.add_argument("-o", "--output", required=False, default='protego_layers.json', help="(Optional) Output file name(default: protego_layers.json)")

    # add/remove/reset fsp
    parser.add_argument("-f", "--function-arn", required=False, default=None, help="(Optional) Function Arn to add/remove/reset Fsp.")

    parser.add_argument(      "--version", required=False, action="store_true", help="Display the protegocli tool version")
    args = parser.parse_args()

    # to enable calling --version without -m
    if not args.version and not args.mode:
        parser.error('argument -m/--mode is required')

    return args


def extract_layer_arn(manifest_data, region, logger, runtime_name=None):
    manifest_reader = ManifestReader(manifest_data, logger)
    return manifest_reader.get_layer_arn(region, runtime_name)

def generate_config(aws_account_id, layers_arns, output, logger):
    config_generator = ConfigGenerator(aws_account_id, layers_arns, logger)
    config_generator.generate(output)


def get_manifest(protego_account_id, fsp_token, fsp_version, logger):
    fsp_downloader = FSPDownloader(protego_account_id, fsp_token, fsp_version, logger)
    return fsp_downloader.get_manifest()


def get_account_id(aws_profile, logger):
    aws_helper = AWSHelper(aws_profile, logger)
    return aws_helper.get_account_id()


def get_layers_arns(region, args, logger, runtime_name=None):
    protego_config = ProtegoConfig(
        args.protego_account_id, args.protego_access_token, logger)

    try:
        manifest_data = get_manifest(
            protego_config.protego_account_id(), protego_config.protego_token(), args.fsp_version, logger)

        layer_arn = extract_layer_arn(manifest_data, region, logger, runtime_name)
        return layer_arn

    except Exception as e:
        logger.error(str(e))
        logger.error_and_exit("Failed to get layers arns. please check your protego account-id and token")


def get_fsp_info(args, logger):
    runtime_name = ProtegoConfig.get_runtime_name(args.runtime)

    if runtime_name is not None and runtime_name not in ["python", "nodejs"]:
        logger.error_and_exit("Invalid runtime : " + str(args.runtime))

    logger.debug("runtime_name: " +  str(runtime_name))

    aws_account_id = get_account_id(args.aws_profile, logger)

    layers_arns = get_layers_arns(args.region, args, logger, runtime_name)

    generate_config(aws_account_id, layers_arns, args.output, logger)


def add_fsp_info(args, logger):
    if args.function_arn is None:
        logger.error_and_exit("function-arn is mandatory argument (-f)")

    try:
        region = ArnLambda(args.function_arn).region
    except ValueError as e:
        logger.error_and_exit("Invalid ARN format. ARN: " + str(args.function_arn))


    aws_account_id = get_account_id(args.aws_profile, logger)

    # we want all the available runtimes layers
    layers_arns = get_layers_arns(region, args, logger, runtime_name=None)

    config_generator = ConfigGenerator(aws_account_id, layers_arns, logger)
    aws_helper = AWSHelper(args.aws_profile, logger)
    aws_helper.add_config_to_function(args.function_arn,
                                      config_generator.get_protego_config())


def remove_fsp_info(args, logger, remove_layer=False):
    if args.function_arn is None:
        logger.error_and_exit("function-arn is mandatory argument (-f)")

    aws_helper = AWSHelper(args.aws_profile, logger)
    aws_helper.remove_config_for_function(args.function_arn, remove_layer=remove_layer)


def main():
    args = get_input_arguments()

    logger = CLILogger(args.quiet, args.verbose)

    if args.version:
        from __init__ import __version__
        logger.info("Version: " + str(__version__))
        return

    logger.print_headline(str(args.mode) + " protego fsp layer")


    if args.mode == "get":
        get_fsp_info(args, logger)
    elif args.mode == "add":
        add_fsp_info(args, logger)
    elif args.mode == "reset":
        remove_fsp_info(args, logger, remove_layer=False)
    elif args.mode == "remove":
        remove_fsp_info(args, logger, remove_layer=True)
    else:
        # should not get here since args parser will catch it before
        logger.error_and_exit("Unknown mode: " + str(args.mode))


if __name__ == "__main__":
    main()
