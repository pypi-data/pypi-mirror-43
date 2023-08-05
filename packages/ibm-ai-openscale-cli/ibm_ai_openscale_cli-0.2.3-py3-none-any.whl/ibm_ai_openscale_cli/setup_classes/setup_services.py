# coding=utf-8
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.utility_classes.utils import jsonFileToDict
import logging

logger = logging.getLogger(__name__)

class SetupServices(object):

    def read_credentials_from_file(self, credentials_file):
        logger.info('Using credentials from "{}"'.format(credentials_file))
        return jsonFileToDict(credentials_file)

    def setup_postgres_database(self):
        if Args.args.postgres is not None:
            logger.info('Compose for PostgreSQL instance specified')
            credentials = self.read_credentials_from_file(Args.args.postgres)
            return credentials
        return None

    def setup_icd_database(self):
        if Args.args.icd is not None:
            logger.info('ICD instance specified')
            credentials = self.read_credentials_from_file(Args.args.icd)
            credentials['db_type'] = 'postgresql'
            connection_data = credentials['connection']['postgres']
            hostname = connection_data['hosts'][0]['hostname']
            port = connection_data['hosts'][0]['port']
            dbname = connection_data['database']
            user = connection_data['authentication']['username']
            password = connection_data['authentication']['password']
            credentials['uri'] = 'postgres://{}:{}@{}:{}/{}'.format(user, password, hostname, port, dbname)
            return credentials
        return None

    def setup_db2_database(self):
        if Args.args.db2 is not None:
            logger.info('DB2 instance specified')
            credentials = self.read_credentials_from_file(Args.args.db2)
            credentials['db_type'] = 'db2'
            return credentials
        return None