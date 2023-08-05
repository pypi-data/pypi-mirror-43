# coding=utf-8
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.setup_classes.setup_services import SetupServices
import logging

logger = logging.getLogger(__name__)

class SetupIBMCloudServices(SetupServices):

    def _aios_credentials(self, data_mart_id):
        aios_credentials = {}
        aios_credentials['apikey'] = Args.args.apikey
        aios_credentials['url'] = Args.env_dict['aios_url']
        aios_credentials['data_mart_id'] = data_mart_id
        return aios_credentials