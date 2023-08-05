# coding=utf-8

import logging
import time
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale import APIClient, APIClient4ICP

logger = logging.getLogger(__name__)

class OpenScale:

    def __init__(self, credentials, database_credentials):
        OpenScale._credentials = credentials
        OpenScale._keep_schema = Args.args.keep_schema
        OpenScale._verify = False if Args.is_icp else True
        OpenScale._database_credentials = database_credentials
        OpenScale._database = self._get_database(database_credentials)
        start = time.time()
        OpenScale._client = APIClient4ICP(credentials) if Args.is_icp else APIClient(credentials)
        elapsed = time.time() - start
        OpenScale._datamart_name = self._get_datamart_name()
        logger.info('Using {} Python Client version: {}'.format(Args.service_name, OpenScale._client.version))
        logger.debug('TIMER: Connect to APIClient in {:.3f} seconds'.format(elapsed))

    def _get_datamart_name(self):
        datamart_name = Args.args.datamart_name
        env_name = Args.env_dict['name'].lower()
        if datamart_name == 'aiosfastpath' and env_name != 'ypprod':
            datamart_name += env_name
        return datamart_name

    def _get_database(self, database_credentials):
        if not database_credentials:
            return None
        if database_credentials['db_type'] == 'postgresql':
            if 'postgres' in database_credentials: # icd
                from ibm_ai_openscale_cli.database_classes.postgres_icd import PostgresICD
                return PostgresICD(database_credentials)
            else: # compose
                from ibm_ai_openscale_cli.database_classes.postgres_compose import PostgresCompose
                return PostgresCompose(database_credentials)
        elif database_credentials['db_type'] == 'db2':
            from ibm_ai_openscale_cli.database_classes.db2 import DB2
            return DB2(database_credentials)
        else:
            raise Exception('Invalid database type specified. Only "postgresql" and "db2" are supported.')