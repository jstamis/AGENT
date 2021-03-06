"""A client that communicates with and provides the capabilities of the flow generation service."""
import os

import requests
import urllib3

from aist_common.log import get_logger

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGER = get_logger('flow-generator-client')


class FlowGeneratorClient:
    """A client that communicates with and provides the capabilities of the flow generation service."""

    FLOW_GEN_URL = "{}/v1/predict"

    def __init__(self):
        """ Initializes the FlowGeneratorClient class.
        """

        self._klass = "FlowGeneratorClient"
        self._set_envs()

    def _set_envs(self):
        """ Loads environment variables.
        """

        self.SERVICE_URL = 'http://flow-generator'
        if 'FLOW_GENERATION_URL' in os.environ:
            self.SERVICE_URL = os.environ['FLOW_GENERATION_URL']

    def generate_flow(self, query):
        """ Communicates with the flow generation service to generate an
            abstract test flow given a precondition.

        :param query: A precondition (e.g. Observe TextBox FirstName).

        :return: A generated abstract test flow.
        """

        url = FlowGeneratorClient.FLOW_GEN_URL.format(self.SERVICE_URL)

        LOGGER.debug("Running flow generator: {}, {}".format(url, query))

        query = [flow_step.lower() for flow_step in query.split(' ')]
        resp = requests.post(url, json=query, verify=False)

        if resp.status_code == 200:
            LOGGER.debug("Successfully ran flow generator.")
            resp = resp.json()
            sequences = resp['sequences']
            if len(sequences) > 0:
                sequence = sequences[0]
                expanded_sequence = " ".join(sequence).upper()

                LOGGER.debug("Generated flow: {}".format(expanded_sequence))

                if expanded_sequence is None:
                    return False

                return expanded_sequence
            return None
        else:
            LOGGER.error("Unable to run flow generator.")
            return False
