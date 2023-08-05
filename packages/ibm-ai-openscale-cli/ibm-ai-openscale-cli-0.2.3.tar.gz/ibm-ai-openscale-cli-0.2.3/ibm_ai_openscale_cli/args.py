# coding=utf-8

class Args:

    service_name = 'Watson OpenScale'

    args = None
    env_dict = None

    is_icp = False

    is_wml = False
    is_azureml = False
    is_spss = False
    is_custom = False
    is_sagemaker = False

    ml_engine_type = None
    ml_engine_display_name = None