# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.setup_classes.setup_ibmcloud_services_cli import SetupIBMCloudServicesCli
from ibm_ai_openscale_cli.setup_classes.setup_ibmcloud_services_rest import SetupIBMCloudServicesRest
from ibm_ai_openscale_cli.setup_classes.setup_ibmcloudprivate_services import SetupIBMCloudPrivateServices

logger = logging.getLogger(__name__)

class Credentials:

    __instance = None

    _services = None
    _ml_engine_credentials = None
    _database_credentials = None
    _openscale_credentials = None
    _cos_credentials = None
    _run_once = True

    @staticmethod
    def get_instance():
        if not Credentials.__instance:
            Credentials.__instance = Credentials()
        return Credentials.__instance

    def __init__(self):
        if Credentials.__instance:
            raise Exception("ERROR: Attempt to create more than one instance. Use Credentials.get_instance() instead")
        else:
            if Args.is_icp:
                Credentials._services = SetupIBMCloudPrivateServices()
            else:
                if Args.args.bx:
                    Credentials._services = SetupIBMCloudServicesCli()
                else:
                    Credentials._services = SetupIBMCloudServicesRest()

    def get_openscale_credentials(self):
        if not Credentials._openscale_credentials:
            Credentials._openscale_credentials = Credentials._services.setup_aios()
        return Credentials._openscale_credentials

    def get_ml_engine_credentials(self):
        if not Credentials._ml_engine_credentials:
            if Args.is_wml:
                Credentials._ml_engine_credentials = Credentials._services.setup_wml()
            if Args.is_azureml:
                Credentials._ml_engine_credentials = Credentials._services.read_credentials_from_file(Args.args.azure)
            if Args.is_spss:
                Credentials._ml_engine_credentials = Credentials._services.read_credentials_from_file(Args.args.spss)
            if Args.is_custom:
                Credentials._ml_engine_credentials = Credentials._services.read_credentials_from_file(Args.args.custom)
            if Args.is_sagemaker:
                Credentials._ml_engine_credentials = Credentials._services.read_credentials_from_file(Args.args.aws)
        return Credentials._ml_engine_credentials

    def get_database_credentials(self):
        if not Credentials._database_credentials and Credentials._run_once:
            # compose
            postgres_credentials = Credentials._services.setup_postgres_database()
            if postgres_credentials is not None:
                Credentials._database_credentials = postgres_credentials
            # icd
            if not Credentials._database_credentials:
                icd_credentials = Credentials._services.setup_icd_database()
                if icd_credentials is not None:
                    Credentials._database_credentials = icd_credentials
            # db2
            if not Credentials._database_credentials:
                db2_credentials = Credentials._services.setup_db2_database()
                if db2_credentials is not None:
                    Credentials._database_credentials = db2_credentials
            Credentials._run_once = False
        return Credentials._database_credentials

    def get_cos_credentials(self):
        if not Credentials._cos_credentials:
            Credentials._cos_credentials = Credentials._services.setup_cos()
        return Credentials._cos_credentials

