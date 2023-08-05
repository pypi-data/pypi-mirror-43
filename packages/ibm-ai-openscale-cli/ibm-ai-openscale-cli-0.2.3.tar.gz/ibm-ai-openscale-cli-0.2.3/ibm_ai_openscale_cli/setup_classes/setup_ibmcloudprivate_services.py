# coding=utf-8
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.setup_classes.setup_services import SetupServices
import logging

logger = logging.getLogger(__name__)

class SetupIBMCloudPrivateServices(SetupServices):

    def setup_aios(self):
        logger.info('Setting up {} instance'.format('Watson OpenScale'))
        aios_icp_credentials = {}
        aios_icp_credentials['username'] = Args.args.username
        aios_icp_credentials['password'] = Args.args.password
        aios_icp_credentials['url'] = '{}'.format(Args.args.url)
        aios_icp_credentials['hostname'] = ':'.join(Args.args.url.split(':')[:2])
        aios_icp_credentials['port'] = Args.args.url.split(':')[2]
        aios_icp_credentials['wml_credentials'] = None
        if Args.args.wml is not None:
            aios_icp_credentials['wml_credentials'] = self.read_credentials_from_file(Args.args.wml)
        return aios_icp_credentials

    def setup_wml(self):
        logger.info('Setting up {} instance'.format('Watson Machine Learning'))
        wml_credentials = {}
        wml_credentials['username'] = Args.args.username
        wml_credentials['password'] = Args.args.password
        wml_credentials['url'] = ':'.join(Args.args.url.split(':')[:2])
        wml_credentials['instance_id'] = 'icp'
        return wml_credentials