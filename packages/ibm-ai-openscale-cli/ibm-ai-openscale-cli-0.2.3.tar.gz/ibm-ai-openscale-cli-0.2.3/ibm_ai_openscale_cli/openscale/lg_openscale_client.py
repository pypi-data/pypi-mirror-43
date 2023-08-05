# coding=utf-8
import time
import logging
import random
from retry import retry
from ibm_ai_openscale_cli.args import Args
from ibm_ai_openscale_cli.openscale.openscale_client import OpenScaleClient

logger = logging.getLogger(__name__)

class LGOpenScaleClient(OpenScaleClient):

    def __init__(self, credentials, database_credentials):
        super().__init__(credentials, database_credentials)

    def get_asset_details(self, deployment_name=None, model_name=None):
        name = model_name if Args.is_wml else deployment_name
        return super().get_asset_details(name)

    @retry(tries=5, delay=4, backoff=2)
    def use_existing_subscription(self, asset_details_dict):
        self._subscribed_deployment_dict = asset_details_dict
        self._subscription = self._client.data_mart.subscriptions.get(asset_details_dict['source_uid'])

    @retry(tries=5, delay=1, backoff=2)
    def _generate_one_scoring_request(self, engine_client, score_input, wml_deployment_url=None):
        start = time.time()
        if Args.is_wml:
            predictions = engine_client.deployments.score(wml_deployment_url, score_input)
        elif Args.is_azureml:
            predictions = engine_client.score(score_input)
        elif Args.is_spss:
            predictions = engine_client.score(score_input)
        elif Args.is_custom:
            predictions = engine_client.score(score_input)
        elif Args.is_sagemaker:
            predictions = engine_client.score(score_input['fields'], score_input['values'])
        end = time.time()
        return (start, end, predictions)

    @retry(tries=5, delay=1, backoff=2)
    # for non-WML engines, the scored payload must be logged
    def _log_payload(self, predictions):
        start = time.time()
        self._subscription.payload_logging.store([predictions])
        end = time.time()
        return (start, end)

    def generate_scoring_requests(self, engine_client=None):
        wml_deployment_url = None
        if Args.is_wml:
            engine_client = self._client.data_mart.bindings.get_native_engine_client(binding_uid=OpenScaleClient._binding_id)
            deployment_details = engine_client.deployments.get_details(self._subscribed_deployment_dict['source_entry_metadata_guid'])
            wml_deployment_url = engine_client.deployments.get_scoring_url(deployment_details)
            if Args.is_icp and ':31002' not in wml_deployment_url:
                deployment_url_host = ':'.join(wml_deployment_url.split(':')[:2])
                args_url_host = ':'.join(Args.env_dict['aios_url'].split(':')[:2])
                wml_deployment_url = wml_deployment_url.replace('{}:16600'.format(deployment_url_host), '{}:31002'.format(args_url_host))
        elif Args.is_azureml:
            engine_client.setup_scoring_metadata(self._subscription)
        elif Args.is_spss:
            engine_client.setup_scoring_metadata(self._subscription)
            subscription_details = self._subscription.get_details()
            model_name_id = subscription_details['entity']['asset']['name']
            input_table_id = subscription_details['entity']['asset_properties']['input_data_schema']['id']
        elif Args.is_custom:
            engine_client.setup_scoring_metadata(self._subscription)
        elif Args.is_sagemaker:
            engine_client.setup_scoring_metadata(self._subscription)

        numscorerequests = Args.args.lg_score_requests
        numscoresperrequest = Args.args.lg_scores_per_request
        pause = Args.args.lg_pause
        lgverbose = Args.args.lg_verbose

        logger.info('Generate {} new scoring requests to {}'.format(numscorerequests, Args.service_name))
        totalelapsed = 0
        firststart = time.time()
        lastend = firststart
        for _ in range(numscorerequests):
            # compose the score request input
            if Args.is_wml:
                fields, values = self._model.get_score_input(numscoresperrequest)
                score_input = {'fields': fields, 'values': values }
            elif Args.is_azureml:
                fields, values = self._model.get_score_input()
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    value_dict[field] = values[index]
                score_input = {'Inputs':{'input1': [value_dict] },'GlobalParameters':{}}
            elif Args.is_spss:
                fields, values = self._model.get_score_input()
                score_input = {'requestInputTable':[{'id': input_table_id, 'requestInputRow':[{'input':[]}]}],'id':model_name_id}
                values = values[0]
                value_dict = {}
                for (index, field) in enumerate(fields):
                    entry_dict = {'name':str(field),'value':str(values[index])}
                    score_input['requestInputTable'][0]['requestInputRow'][0]['input'].append(entry_dict)
            elif Args.is_custom:
                fields, values = self._model.get_score_input()
                score_input = {'fields': fields, 'values': values }
            elif Args.is_sagemaker:
                fields, values = self._model.get_score_input_sagemaker()
                score_input = {'fields': fields, 'values': values }

            # make the score request
            (start, end, predictions) = self._generate_one_scoring_request(engine_client, score_input, wml_deployment_url)
            elapsed = end - start
            totalelapsed += elapsed
            lastend = end
            if lgverbose:
                logger.info('Request {} scores(s) in {:.3f} seconds'.format(numscoresperrequest, elapsed))

            # for non-WML engines, the scored payload must be logged
            if not Args.is_wml:
                (start, end) = self._log_payload(predictions)
                elapsed = end - start
                totalelapsed += elapsed
                lastend = end
                if lgverbose:
                    logger.info('Log payload in {:.3f} seconds'.format(elapsed))
            if pause > 0.0:
                time.sleep(pause)
        if numscorerequests > 0:
            duration = lastend - firststart
            logger.info('Total score requests: {}, total scores: {}, duration: {:.3f} seconds'.format(numscorerequests, numscorerequests*numscoresperrequest, duration))
            logger.info('Throughput: {:.3f} score requests per second, {:.3f} scores per second, average score request time: {:.3f} seconds'.format(numscorerequests/duration, numscorerequests*numscoresperrequest/duration, totalelapsed/numscorerequests))

    @retry(tries=5, delay=1, backoff=2)
    def _generate_one_explain(self, scoring_id):
        start = time.time()
        explain = self._subscription.explainability.run(scoring_id, background_mode=True)
        end = time.time()
        return (start, end, explain)

    @retry(tries=5, delay=4, backoff=2)
    def _get_available_scores(self, max_explain_candidates):
        start = time.time()
        payload_table = self._subscription.payload_logging.get_table_content(format='pandas', limit=max_explain_candidates)
        end = time.time()
        scoring_ids = []
        for index, row in payload_table.iterrows():
            scoring_ids.append(row['scoring_id'])
        random.shuffle(scoring_ids)
        return (start, end, scoring_ids)

    def generate_explain_requests(self):
        numexplainrequests = Args.args.lg_explain_requests
        pause = Args.args.lg_pause
        lgverbose = Args.args.lg_verbose
        logger.info('Generate {} explain requests to {}'.format(numexplainrequests, Args.service_name))
        if numexplainrequests < 1:
            return
        (start, end, scoring_ids) = self._get_available_scores(Args.args.lg_max_explain_candidates)
        elapsed = end - start
        logger.info('Found {} available scores for explain, in {:.3f} seconds'.format(len(scoring_ids), elapsed))
        if numexplainrequests > len(scoring_ids):
            numexplainrequests = len(scoring_ids)

        if Args.args.lg_explain_sync:
            input('Press ENTER to start generating explain requests')

        totalelapsed = 0
        firststart = time.time()
        lastend = firststart

        for i in range(numexplainrequests):
            scoring_id = scoring_ids[i]
            (start, end, explain) = self._generate_one_explain(scoring_id)
            elapsed = end - start
            totalelapsed += elapsed
            lastend = end
            if lgverbose:
                logger.info('Request explain in {:.3f} seconds, scoring_id: {}, explain_id: {}'.format(elapsed, scoring_id, explain['metadata']['id']))
            if pause > 0.0:
                time.sleep(pause)

        duration = lastend - firststart
        logger.info('Total explain requests: {}, duration: {:.3f} seconds'.format(numexplainrequests, duration))
        logger.info('Throughput: {:.3f} explain requests per second, average explain request time: {:.3f} seconds'.format(numexplainrequests/duration, totalelapsed/numexplainrequests))

    @retry(tries=5, delay=4, backoff=2)
    def trigger_monitors(self):
        if Args.args.lg_checks:
            background_mode = not Args.args.sync_checks
            lgverbose = Args.args.lg_verbose
            time.sleep(5.0) # pause 5 seconds to give time for payload logging to finish for any just-completed scores
            logger.info('Trigger immediate fairness check')
            start = time.time()
            self._subscription.fairness_monitoring.run(background_mode=background_mode)
            end = time.time()
            logger.info('Trigger fairness check in {:.3f} seconds'.format(end - start))
            logger.info('Trigger immediate quality check')
            start = time.time()
            self._subscription.quality_monitoring.run(background_mode=background_mode)
            end = time.time()
            logger.info('Trigger quality check in {:.3f} seconds'.format(end - start))
