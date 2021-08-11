from ncdssdk.src.main.python.ncdsclient.internal.utils.KafkaConfigLoader import KafkaConfigLoader
import json


def test_load_test_config():
    kafka_config = KafkaConfigLoader()

    cfg = {}
    with open("../resources/pytest-config.json", "r") as f:
        cfg = json.load(f)
    f.close()

    assert kafka_config.load_test_config() == cfg
