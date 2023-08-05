# coding=utf-8
from __future__ import print_function
import argparse
import logging
import urllib3
from ibm_ai_openscale_cli import logging_temp_file, name
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.environments import Environments
from ibm_ai_openscale_cli.openscale.openscale_reset import ResetType
from ibm_ai_openscale_cli.openscale_ops import OpenScaleOps
from ibm_ai_openscale_cli.reset_ops import ResetOps
from ibm_ai_openscale_cli.version import __version__
from outdated import warn_if_outdated

logger = logging.getLogger(__name__)

def get_argument_parser():
    """
    generate a CLI arguments parser
    Returns:
       argument parser
    """
    parser = argparse.ArgumentParser()
    # required parameters
    requiredArgs = parser.add_argument_group('required arguments')
    requiredArgs.add_argument('-a', '--apikey', help='IBM Cloud APIKey', required=True)
    # Optional parameters
    optionalArgs = parser._action_groups.pop()
    parser.add_argument('--env', default='ypprod', help='Environment. Default "ypprod"', choices=['ypprod', 'ypqa', 'ys1dev', 'icp'])
    parser.add_argument('--resource-group', default='default', help='Resource Group to use. If not specified, then "default" group is used')
    parser.add_argument('--postgres', help='Path to postgres credentials file for the datamart database. If --postgres, --icd, and --db2 all are not specified, then the internal {} database is used'.format(Args.service_name))
    parser.add_argument('--icd', help='Path to IBM Cloud Database credentials file for the datamart database')
    parser.add_argument('--db2', help='Path to IBM DB2 credentials file for the datamart database')
    parser.add_argument('--wml', help='Path to IBM WML credentials file')
    parser.add_argument('--azure', help='Path to Microsoft Azure credentials file')
    parser.add_argument('--spss', help='Path to SPSS credentials file')
    parser.add_argument('--custom', help='Path to Custom Engine credentials file')
    parser.add_argument('--aws', help='Path to Amazon Web Services credentials file')
    parser.add_argument('--deployment-name', help='Name of the deployment to use. Required for Azure ML Studio, SPSS Engine and Custom ML Engine')
    parser.add_argument('--username', help='ICP username. Required if "icp" environment is chosen')
    parser.add_argument('--password', help='ICP password. Required if "icp" environment is chosen')
    parser.add_argument('--url', help='ICP url. Required if "icp" environment is chosen')
    parser.add_argument('--datamart-name', default='aiosfastpath', help='Specify data mart name and schema, default is "aiosfastpath"')
    parser.add_argument('--keep-schema', action='store_true', help='Use pre-existing datamart schema, only dropping all tables. If not specified, datamart schema is dropped and re-created')
    parser.add_argument('--history', default=7, help='Days of history to preload. Default is 7', type=int)
    parser.add_argument('--verbose', action='store_true', help='verbose flag')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('--model', default='GermanCreditRiskModel', help='Model to set up with Watson OpenScale (default "GermanCreditRiskModel")', choices=['all', 'GermanCreditRiskModel', 'DrugSelectionModel', 'GolfModel'])
    parser.add_argument('--training-data-json', help=argparse.SUPPRESS)
    parser.add_argument('--bx', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--extend', action='store_true', help=argparse.SUPPRESS) # Extend existing datamart. If not specified and the datamart already exists, it will be deleted and recreated. Currently only supported for WML.
    parser.add_argument('--reset', choices=['metrics', 'monitors', 'datamart', 'model'], help='Reset existing datamart then exit')
    parser.add_argument('--model-first-instance', default=1, help=argparse.SUPPRESS, type=int) # First "instance" (copy) of each model. Default 1 means to start with the base model instance
    parser.add_argument('--model-instances', default=1, help=argparse.SUPPRESS, type=int) # Number of additional instances beyond the first.
    parser.add_argument('--sync-checks', action='store_true', help=argparse.SUPPRESS) # If true, make fairness and quality checks synchronous (default is asynchronous)
    parser.add_argument('--organization', help=argparse.SUPPRESS, required=False)
    parser.add_argument('--space', help=argparse.SUPPRESS, required=False)
    parser._action_groups.append(optionalArgs)
    return parser

def process_args(parser):
    """
    Parses the parser
    Returns:
        dict -- dictionary with the arguments and values
    """
    args = parser.parse_args()

    # validate environment
    if 'throw' in args:
        logger.error(args.throw)
        exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('handle_response').setLevel(logging.DEBUG)
        logging.getLogger('ibm_ai_openscale.utils.client_errors').setLevel(logging.DEBUG)

    if (args.postgres and args.icd) or (args.postgres and args.db2) or (args.icd and args.db2):
        logger.error('ERROR: Only one datamart database option can be specified')
        exit(1)

    if args.reset:
        args.reset = ResetType(args.reset)

    return args

def initialize(args):
    """
    Initialize and validate necessary entities
    """
    # setup the loger
    logger.info('ibm-ai-openscale-cli-{}'.format(__version__))
    logger.info('Log file: {0}'.format(logging_temp_file.name))

    # outdated packages
    warn_if_outdated(name, __version__)

    # args validation
    def _validate_deployment_name_specified(deployment_name, model_name=None, env_name='ypprod'):
        if Args.is_wml:
            if deployment_name and model_name == 'all':
                logger.error('ERROR: A model name is required when a deployment is specified for {}'.format(Args.ml_engine_display_name))
                exit(1)
        else:
            if not deployment_name:
                logger.error('ERROR: A deployment name is required when {} is used with {}'.format(Args.service_name, Args.ml_engine_display_name))
                exit(1)

    def _validate_is_icp(env_name):
        if not env_name == 'icp':
            logger.error('ERROR: {} is only supported on {} on IBM Cloud Private (ICP)'.format(Args.service_name, Args.ml_engine_display_name))
            exit(1)

    if args.azure:
        Args.is_azureml = True
        Args.ml_engine_type = 'azureml'
        Args.ml_engine_display_name = 'Microsoft Azure Machine Learning'
        _validate_deployment_name_specified(args.deployment_name)
    elif args.spss:
        Args.is_spss = True
        Args.ml_engine_type = 'spss'
        Args.ml_engine_display_name = 'IBM SPSS C&DS'
        _validate_is_icp(args.env)
        _validate_deployment_name_specified(args.deployment_name)
    elif args.custom:
        Args.is_custom = True
        Args.ml_engine_type = 'custom'
        Args.ml_engine_display_name = 'Custom Machine Learning'
        _validate_deployment_name_specified(args.deployment_name)
    elif args.aws:
        Args.is_sagemaker = True
        Args.ml_engine_type = 'sagemaker'
        Args.ml_engine_display_name = 'Amazon SageMaker Machine Learning'
        _validate_deployment_name_specified(args.deployment_name)
    else:
        Args.is_wml = True
        Args.ml_engine_type = 'wml'
        Args.ml_engine_display_name = 'IBM Watson Machine Learning'
        _validate_deployment_name_specified(args.deployment_name, args.model, args.env)

    env_dict = Environments(args).get_attributes()
    Args.args = args
    Args.env_dict = env_dict
    if args.env == 'icp':
        Args.is_icp = True
        logger.info('SSL verification is not used for requests against ICP Environment, disabling "InsecureRequestWarning"')
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def show_finish_prompt():
    logger.info('Process complete')
    dashboard_url = Args.env_dict['aios_url']
    if dashboard_url.startswith('https://api.'):
        dashboard_url = dashboard_url.replace('https://api.', 'https://')
    logger.info('The {} dashboard can be accessed at: {}/aiopenscale'.format(Args.service_name, dashboard_url))

def main():

    parser = get_argument_parser()
    args = process_args(parser)
    initialize(args)

    # operations
    if args.reset:
        ResetOps().execute()
    else:
        OpenScaleOps().execute()

    # finish
    show_finish_prompt()

