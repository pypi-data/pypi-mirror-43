# coding=utf-8

import logging
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.credentials import Credentials
from ibm_ai_openscale_cli.ml_engines.azure_machine_learning import AzureMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.custom_machine_learning import CustomMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.sagemaker_machine_learning import SageMakerMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.spss_machine_learning import SPSSMachineLearningEngine
from ibm_ai_openscale_cli.ml_engines.watson_machine_learning import WatsonMachineLearningEngine
from ibm_ai_openscale_cli.models.drug_selection_model import DrugSelectionModel
from ibm_ai_openscale_cli.models.german_credit_risk_model import GermanCreditRiskModel
from ibm_ai_openscale_cli.models.scikit_digits_model import ScikitDigitsModel
from ibm_ai_openscale_cli.models.golf_model import GolfModel

logger = logging.getLogger(__name__)

class Ops:

    _credentials = None
    _wml_modelnames = ['DrugSelectionModel', 'GermanCreditRiskModel', 'GolfModel'] # suppress ScikitDigitsModel for now
    _azure_modelnames = ['GermanCreditRiskModel']
    _spss_modelnames = ['GermanCreditRiskModel']
    _custom_modelnames = ['GermanCreditRiskModel']
    _sagemaker_modelnames = ['GermanCreditRiskModel']

    _ml_engine = None

    def __init__(self):
        Ops._credentials = Credentials.get_instance()

    def get_modeldata_instance(self, modelname, model_instance_num):
        model = None
        if modelname == 'DrugSelectionModel':
            model = DrugSelectionModel(model_instance_num)
        elif modelname == 'GermanCreditRiskModel':
            model = GermanCreditRiskModel(model_instance_num)
        elif modelname == 'ScikitDigitsModel':
            model = ScikitDigitsModel(model_instance_num) # temporarily, don't load history
        elif modelname == 'GolfModel':
            model = GolfModel(model_instance_num) # temporarily, don't load history
        return model

    def get_ml_engine_instance(self):
        if not Ops._ml_engine:
            ml_engine_credentials = Ops._credentials.get_ml_engine_credentials()
            if Args.is_wml:
                Ops._ml_engine = WatsonMachineLearningEngine(ml_engine_credentials)
            elif Args.is_azureml:
                Ops._ml_engine = AzureMachineLearningEngine()
            elif Args.is_spss:
                Ops._ml_engine = SPSSMachineLearningEngine(ml_engine_credentials)
            elif Args.is_custom:
                Ops._ml_engine = CustomMachineLearningEngine(ml_engine_credentials)
            elif Args.is_sagemaker:
                Ops._ml_engine = SageMakerMachineLearningEngine(ml_engine_credentials)
        return Ops._ml_engine
