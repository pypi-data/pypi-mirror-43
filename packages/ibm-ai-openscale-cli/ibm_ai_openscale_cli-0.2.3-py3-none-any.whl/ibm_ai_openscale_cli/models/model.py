# coding=utf-8
import logging
import os
import datetime
import random
import math
import json
import pandas as pd
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale.supporting_classes import BluemixCloudObjectStorageReference
from ibm_ai_openscale_cli.utility_classes.utils import jsonFileToDict
from pathlib import Path

logger = logging.getLogger(__name__)

class Model():

    CONFIGURATION_FILENAME = 'configuration.json'
    MODEL_META_FILENAME = 'model_meta.json'
    MODEL_CONTENT_FILENAME = 'model_content.gzip'
    PIPELINE_META_FILENAME = 'pipeline_meta.json'
    PIPELINE_CONTENT_FILENAME = 'pipeline_content.gzip'
    TRAINING_DATA_STATISTICS_FILENAME = 'training_data_statistics.json'
    FAIRNESS_HISTORY_FILENAME = 'history_fairness.json'
    PAYLOAD_HISTORY_FILENAME = 'history_payloads.json'
    TRAINING_DATA_CSV_FILENAME = 'training_data.csv'
    DEBIAS_HISTORY_FILENAME = 'history_debias.json'
    MANUAL_LABELING_HISTORY_FILENAME = 'history_manual_labeling.json'

    def __init__(self, name, model_instances=1, training_data_dict=None, training_data_type=None):
        self.name = name
        if model_instances > 1:
            self.name += str(model_instances)
        self._model_dir = os.path.join(os.path.dirname(__file__), name)
        env_name = '' if Args.env_dict['name'] == 'YPPROD' else Args.env_dict['name']

        # model create and deploy
        self.metadata = {}
        self.metadata['model_name'] = self.name + env_name
        self.metadata['model_metadata_file'] = self._get_file_path(Model.MODEL_META_FILENAME)
        self.metadata['model_file'] = self._get_file_path(Model.MODEL_CONTENT_FILENAME)
        self.metadata['pipeline_metadata_file'] = self._get_file_path(Model.PIPELINE_META_FILENAME)
        self.metadata['pipeline_file'] = self._get_file_path(Model.PIPELINE_CONTENT_FILENAME)
        self.metadata['deployment_name'] = self.name + env_name
        self.metadata['deployment_description'] = 'Created by Watson OpenScale Fast Path.'

        # configuration
        configuration_file = self._get_file_path(Model.CONFIGURATION_FILENAME)
        if configuration_file:
            self.configuration_data = jsonFileToDict(configuration_file)
        else:
            logger.error('ERROR: Unable to find configuration file: {}'.format(configuration_file))
            exit(1)

        # training data
        self.training_data_reference = None
        self.training_data = None
        self.training_data_statistics = None
        if training_data_dict:
            self._cos_credentials = training_data_dict['connection']
            self._training_data_filename = training_data_dict['source']['file_name']
            self._bucket_name = training_data_dict['source']['bucket']
            first_line_header = True if training_data_dict['source']['firstlineheader'] == 'true' else False
            self.training_data_reference = BluemixCloudObjectStorageReference( self._cos_credentials,
                                        '{}/{}'.format( self._bucket_name,
                                                        self._training_data_filename ),
                                        first_line_header=first_line_header )
        else:
            statistics_file = self._get_file_path(Model.TRAINING_DATA_STATISTICS_FILENAME)
            if statistics_file:
                self.training_data_statistics = jsonFileToDict(statistics_file)
            else:
                training_data_file = self._get_file_path(Model.TRAINING_DATA_CSV_FILENAME)
                if training_data_file:
                    self.training_data = pd.read_csv(training_data_file, dtype=training_data_type)



    def _get_file_path(self, filename):
        """
        Returns the path for the file for the current serve engine, else the common file
        Eg. /path/to/sagemaker/training_data_statistics.json OR /path/to/training_data_statistics.json OR None
        """
        engine_specific_path = os.path.join(self._model_dir, Args.ml_engine_type, filename)
        if Path(engine_specific_path).is_file():
            return engine_specific_path
        else:
            path = os.path.join(self._model_dir, filename)
            if Path(path).is_file():
                return path
        return None

    def _get_score_time(self, day, hour):
        return datetime.datetime.utcnow() + datetime.timedelta(hours=(-(24 * day + hour + 1)))

    # return an array of tuples with datestamp, response_time, and records
    def get_performance_history(self, num_day):
        fullRecordsList = []
        now = datetime.datetime.utcnow()
        for day in range(num_day, num_day+1):
            # model "typical" day (min at midnight, max at noon)
            # but with some days more busy overall than others, plus some random "noise"
            day_base = random.randint(1,4)
            for hour in range(24):
                score_time = (now + datetime.timedelta(hours=(-(24 * day + hour + 1)))).strftime('%Y-%m-%dT%H:%M:%SZ')
                score_count = day_base*60 + math.fabs(hour - 12)*30*random.randint(1,2) + 2*random.randint(-30, 90) + 1
                score_resp = random.uniform(60, 300)
                fullRecordsList.append({'timestamp': score_time, 'value': {'response_time': score_resp, 'records': score_count}})
        return fullRecordsList

    def get_fairness_history(self, num_day):
        historyfile = os.path.join(self._model_dir, Model.FAIRNESS_HISTORY_FILENAME)
        fullRecordsList = []
        if historyfile != None:
            with open(historyfile) as f:
                fairnessValues = json.load(f)
            for day in range(num_day, num_day+1):
                for hour in range(24):
                    score_time = self._get_score_time(day, hour).strftime('%Y-%m-%dT%H:%M:%SZ')
                    fullRecordsList.append({'timestamp': score_time, 'value': fairnessValues[random.randint(0, len(fairnessValues))-1]})
        return fullRecordsList

    def get_debias_history(self, num_day):
        fullRecordsList = []
        return fullRecordsList

    def get_quality_history(self, num_day, quality_min, quality_max):
        fullRecordsList = []
        for day in range(num_day, num_day+1):
            for hour in range(24):
                qualityTime = self._get_score_time(day, hour).strftime('%Y-%m-%dT%H:%M:%SZ')
                quality = random.uniform(quality_min, quality_max)
                fullRecordsList.append({
                    'timestamp': qualityTime,
                    'value': {
                        'quality': quality,
                        'threshold': 0.8,
                        'metrics': [{
                            'name': 'auroc',
                            'value': quality,
                            'threshold': 0.8
                        }]
                    }
                })
        return fullRecordsList

    def get_manual_labeling_history(self, num_day):
        fullRecordsList = []
        return fullRecordsList
