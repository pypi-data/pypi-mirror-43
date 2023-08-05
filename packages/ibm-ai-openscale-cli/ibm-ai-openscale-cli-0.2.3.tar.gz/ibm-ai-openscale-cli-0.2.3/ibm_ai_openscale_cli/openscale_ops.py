# coding=utf-8
from __future__ import print_function
import logging
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient
from ibm_ai_openscale_cli.openscale.openscale_reset import ResetType
from ibm_ai_openscale_cli.ops import Ops

logger = logging.getLogger(__name__)

class OpenScaleOps(Ops):

    def __init__(self):
        super().__init__()
        self._model_names = Ops._wml_modelnames

    def _validate_model_name(self):
        def _is_model_name_valid(valid_names_list):
            if Args.args.model not in valid_names_list:
                logger.error('Invalid model name specified. Only the following models are supported {}: {}'.format(Args.ml_engine_display_name, valid_names_list))
                exit(1)
        if Args.is_azureml:
            _is_model_name_valid(valid_names_list=Ops._azure_modelnames)
        elif Args.is_spss:
            _is_model_name_valid(valid_names_list=Ops._spss_modelnames)
        elif Args.is_custom:
            _is_model_name_valid(valid_names_list=Ops._custom_modelnames)
        elif Args.is_sagemaker:
            _is_model_name_valid(valid_names_list=Ops._sagemaker_modelnames)
        elif Args.is_wml:
            _is_model_name_valid(valid_names_list=Ops._wml_modelnames)

    def execute(self):

        # validations
        if Args.args.model != 'all':
            self._validate_model_name()
            self._model_names = [Args.args.model]

        # instantiate openscale
        openscale_credentials = Ops._credentials.get_openscale_credentials()
        database_credentials = Ops._credentials.get_database_credentials()
        openscale_client = OpenScaleClient(openscale_credentials, database_credentials)

        # Instantiate ml engine
        logger.info('Using {}'.format(Args.ml_engine_display_name))
        ml_engine = self.get_ml_engine_instance()

        if not Args.is_icp:
            logger.debug('Watson OpenScale data mart id: {}'.format(openscale_credentials['data_mart_id']))

        # reset datamart if not extending
        if not Args.args.extend:
            logger.info('Reset datamart if already present: {}'.format(Args.args.datamart_name))
            openscale_client.reset(ResetType.DATAMART)
            openscale_client.create_datamart()
            ml_engine_credentials = Ops._credentials.get_ml_engine_credentials()
            openscale_client.bind_mlinstance(ml_engine_credentials)

        modeldata = None
        run_once = True
        for modelname in self._model_names:
            logger.info('--------------------------------------------------------------------------------')
            logger.info('Model: {}, Engine: {}'.format(modelname, Args.ml_engine_display_name))
            logger.info('--------------------------------------------------------------------------------')
            for model_instance_num in range(Args.args.model_first_instance, Args.args.model_first_instance + Args.args.model_instances):

                # model instance
                modeldata = self.get_modeldata_instance(modelname, model_instance_num)
                openscale_client.set_model(modeldata)

                asset_details_dict = None
                # ml engine instance
                if Args.is_wml:
                    ml_engine.set_model(modeldata)
                    if not Args.args.deployment_name:
                        asset_details_dict = ml_engine.create_model_and_deploy()
                    else:
                        asset_details_dict = ml_engine.get_existing_deployment(Args.args.deployment_name)
                else:
                    asset_details_dict = openscale_client.get_asset_details(Args.args.deployment_name)

                if Args.args.extend and run_once:
                    run_once = False
                    openscale_client.use_existing_binding(asset_details_dict)

                # ai openscale operations
                openscale_client.subscribe_to_model_deployment(asset_details_dict)
                openscale_client.configure_subscription()
                openscale_client.payload_logging()
                openscale_client.configure_subscription_monitors()
                openscale_client.generate_sample_metrics()
                openscale_client.generate_sample_scoring(ml_engine)
                openscale_client.trigger_monitors()
