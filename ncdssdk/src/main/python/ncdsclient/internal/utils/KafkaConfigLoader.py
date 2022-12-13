from ncdssdk.src.main.python.ncdsclient.internal.utils.IsItPyTest import is_py_test
import ncdssdk.src.tests.resources as sysresources
import json

from importlib import resources
import logging


class KafkaConfigLoader:
    """
    Utility to load the kafka configuration parameters.
    """

    def __init__(self):
        self.BOOTSTRAP_SERVERS = "bootstrap.servers"
        self.AUTO_OFFSET_RESET_CONFIG = 'auto.offset.reset'
        self.GROUP_ID_CONFIG = 'group.id'
        self.TIMEOUT = 'timeout'
        self.NUM_MESSAGES = 'num_messages'
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def load_test_config():
        cfg = {}

        with resources.open_text(sysresources, "pytest-config.json") as f:
            cfg = json.load(f)
        f.close()

        return cfg

    @staticmethod
    def nasdaq_specific_config(p):
        if not is_py_test():
            p["security.protocol"] = "SASL_SSL"
            p["sasl.mechanism"] = "OAUTHBEARER"
            p["ssl.endpoint.identification.algorithm"] = "https"

        return p

    def validate_and_add_specific_properties(self, p):
        if not p[self.BOOTSTRAP_SERVERS]:
            raise Exception(
                "bootstrap.servers Properties is not set in the Kafka Configuration")
        if not p[self.AUTO_OFFSET_RESET_CONFIG]:
            self.AUTO_OFFSET_RESET_CONFIG = "earliest"
        if self.TIMEOUT not in p:
            p[self.TIMEOUT] = 10
        if self.NUM_MESSAGES not in p:
            p[self.NUM_MESSAGES] = 500

        self.nasdaq_specific_config(p)
        return p
