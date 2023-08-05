# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.main import initialize, show_finish_prompt, get_argument_parser
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.lg_ops import LGOps

logger = logging.getLogger(__name__)

def process_args(parser):
    """
    Parse the CLI arguments
    Returns:
        dict -- dictionary with the arguments and values
    """

    lgArgs = parser._action_groups.pop()
    parser.add_argument('--lg-model-instance-num', default=1, help='Model instance number (default = 1)', type=int)
    parser.add_argument('--lg-score-requests', default=0, help='Number of score requests (default = 0)', type=int)
    parser.add_argument('--lg-scores-per-request', default=1, help='Number of scores per score request (default = 1). Values greater than 1 only supported for WML deployments', type=int)
    parser.add_argument('--lg-explain-requests', default=0, help='Number of explain requests (default = 0)', type=int)
    parser.add_argument('--lg-max-explain-candidates', default=1000, help='Maximum number of candidate scores for explain (default = 1000)', type=int)
    parser.add_argument('--lg-explain-sync', action='store_true', help='User input initiates sending explain requests')
    parser.add_argument('--lg-pause', default=0.0, help='Pause in seconds between requests (default = 0.0)', type=float)
    parser.add_argument('--lg-verbose', action='store_true', help='Display individual request response times')
    parser.add_argument('--lg-checks', action='store_true', help='Trigger fairness and quality checks')
    parser._action_groups.append(lgArgs)

    args = parser.parse_args()

    # validate environment
    if 'throw' in args:
        logger.error(args.throw)
        exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('handle_response').setLevel(logging.DEBUG)
        logging.getLogger('ibm_ai_openscale.utils.client_errors').setLevel(logging.DEBUG)

    return args

def main():

    parser = get_argument_parser()
    args = process_args(parser)
    initialize(args)

    if not Args.args.deployment_name:
        logger.error('ERROR: LG requires a deployment_name be specified')
        exit(1)
    if (Args.args.lg_scores_per_request > 1) and (not Args.is_wml):
        logger.error('ERROR: Scores per request > 1 only supported for WML deployments')
        exit(1)

    # operations
    LGOps().execute()

    # finish
    show_finish_prompt()
