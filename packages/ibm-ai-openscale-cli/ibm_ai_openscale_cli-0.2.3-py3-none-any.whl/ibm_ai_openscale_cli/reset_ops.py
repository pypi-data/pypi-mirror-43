# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient
from ibm_ai_openscale_cli.openscale.openscale_reset import ResetType
from ibm_ai_openscale_cli.ops import Ops

logger = logging.getLogger(__name__)

class ResetOps(Ops):

    def __init__(self):
        super().__init__()

    def _reset_model(self):
        ml_engine = self.get_ml_engine_instance()
        for modelname in Ops._wml_modelnames:
            logger.info('--------------------------------------------------------------------------------')
            logger.info('Model: {}, Engine: {}'.format(modelname, Args.ml_engine_display_name))
            logger.info('--------------------------------------------------------------------------------')
            for model_instance_num in range(Args.args.model_first_instance, Args.args.model_first_instance + Args.args.model_instances):
                modeldata = self.get_modeldata_instance(modelname, model_instance_num)
                ml_engine.set_model(modeldata)
                ml_engine.model_cleanup()

    def _reset_openscale(self):
        openscale_credentials = Ops._credentials.get_openscale_credentials()
        database_credentials = Ops._credentials.get_database_credentials()
        openscale_client = OpenScaleClient(openscale_credentials, database_credentials)
        openscale_client.reset(Args.args.reset)

    def execute(self):
        if Args.args.reset is ResetType.MODEL and Args.is_wml:
            self._reset_model()
        else:
            self._reset_openscale()
