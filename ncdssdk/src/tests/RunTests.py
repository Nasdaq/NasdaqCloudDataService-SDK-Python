from functools import partial
from pathlib import Path
from subprocess import Popen
from typing import Tuple
from time import sleep
import subprocess

from pytest_kafka import (
    make_zookeeper_process, make_kafka_server, make_kafka_consumer,
    terminate,
)

ROOT = Path(__file__).parent.parent.parent.parent
THIS_DIR = Path(__file__).parent
KAFKA_SCRIPTS = ROOT / 'kafka/bin/'
KAFKA_BIN = str(KAFKA_SCRIPTS / 'kafka-server-start.sh')
ZOOKEEPER_BIN = str(KAFKA_SCRIPTS / 'zookeeper-server-start.sh')

# You can pass a custom teardown function (or parametrise ours). Just don't call it `teardown`
# or Pytest will interpret it as a module-scoped teardown function.
teardown_fn = partial(terminate, signal_fn=Popen.kill)
zookeeper_proc = make_zookeeper_process(ZOOKEEPER_BIN, teardown_fn=teardown_fn, zk_port=2181)
kafka_server = make_kafka_server(KAFKA_BIN, 'zookeeper_proc', teardown_fn=teardown_fn, kafka_port=9092)


def test_integration(kafka_server: Tuple[Popen, int]):
    RUN_TESTS_CMD = ['pytest', '-s', THIS_DIR / 'NCDSSDKPyTest.py']
    test_process = subprocess.Popen(RUN_TESTS_CMD)
    test_process.wait()
    delete_test_topics()
    sleep(5)


def delete_test_topics():
    delete_ctrl_topic_cmd = [str(KAFKA_SCRIPTS) +
                             "/kafka-topics.sh", "--zookeeper", "localhost:2181", "--delete", "--topic", "control"]
    delete_mock_topic_cmd = [str(KAFKA_SCRIPTS) +
                             "/kafka-topics.sh", "--zookeeper", "localhost:2181", "--delete", "--topic",
                             "MOCK.stream"]
    delete_gids_topic_cmd = [str(KAFKA_SCRIPTS) +
                             "/kafka-topics.sh", "--zookeeper", "localhost:2181", "--delete", "--topic",
                             "GIDS.stream"]
    subprocess.Popen(delete_ctrl_topic_cmd)
    subprocess.Popen(delete_mock_topic_cmd)
    subprocess.Popen(delete_gids_topic_cmd)