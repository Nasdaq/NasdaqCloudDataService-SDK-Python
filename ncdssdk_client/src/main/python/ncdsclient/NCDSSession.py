import json
import click
import sys
import logging
from ncdssdk.src.main.python.ncdsclient.NCDSClient import NCDSClient
from ncdssdk_client.src.main.python.ncdsclient.utils.ValidateInput import ValidateInput
from confluent_kafka import KafkaException
from importlib import resources
import ncdssdk_client.src.main.python.resources as configresources
import ncdssdk.src.main.resources as sysresources
from ncdssdk.src.main.python.ncdsclient.internal.utils import ConsumerConfig
import logging


class NCDSSession:

    def __init__(self, cmd):
        self.cmd = cmd
        self.test_option = cmd['opt']
        self.topic = cmd['topic']
        self.symbols = cmd['symbols']
        self.msgnames = cmd['msgnames']
        self.message_name = cmd['msgname']
        self.num_top_messages = cmd['n']
        self.timestamp = cmd['timestamp']

        self.auth_props_file = cmd['authprops']
        self.kafka_props_file = cmd['kafkaprops']
        self.security_cfg = None
        self.kafka_cfg = None
        self.logger = logging.getLogger(__name__)

        self.logger = logging.getLogger(__name__)

    def main(self):
        self.security_cfg = load_auth_properties(self.auth_props_file)
        self.kafka_cfg = load_kafka_config(self.kafka_props_file)

        cmd_to_validate = ValidateInput(self.cmd)
        cmd_to_validate.validate_user_input()

        ncds_client = None

        try:
            if self.test_option == "TOP":
                self.top_cmd()

            elif self.test_option == "SCHEMA":
                ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
                # Dump the Schema for the self.topic
                schema = ncds_client.get_schema_for_topic(self.topic)
                print("Schema for the Topic:" + self.topic)
                if schema:
                    print(schema)
                else:
                    print(" Access to topic is not granted ")

            elif self.test_option == "GETMSG":
                ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
                print("Finding the message")
                if "auto.offset.reset" in self.kafka_cfg and self.kafka_cfg["auto.offset.reset"] == "latest":
                    print("Need to get run GETMSG with 'earliest' offset")
                    sys.exit(0)
                msg = ncds_client.get_sample_messages(
                    self.topic, self.message_name, False)
                if msg is not None:
                    print(msg)
                else:
                    print("Message Not Found ...")

            elif self.test_option == "GETALLMSGS":
                ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
                print("Finding the messages")
                if "auto.offset.reset" in self.kafka_cfg and self.kafka_cfg["auto.offset.reset"] == "latest":
                    print("Need to run GETMSG with 'earliest' offset")
                    sys.exit(0)
                ncds_client.get_sample_messages(
                    self.topic, self.message_name, True)

            elif self.test_option == "TOPICS":
                ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
                self.topics = ncds_client.list_topics_for_client()
                print("List of streams available on Nasdaq Cloud Data Service:")
                for self.topic in self.topics:
                    print(self.topic)

            elif self.test_option == "CONTSTREAM":
                self.cont_stream_cmd()

            elif self.test_option == "FILTERSTREAM":
                self.filter_stream_cmd()
        except Exception as e:
            logging.exception(e)

    def top_cmd(self):
        ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
        numOfRecords = max(10, min(int(self.num_top_messages), 999))
        records = ncds_client.top_messages(
            self.topic) if not self.timestamp else ncds_client.top_messages(self.topic, self.timestamp)
        print("Top " + str(numOfRecords) +
              " Records for the Topic: " + self.topic)
        if records:
            if len(records) == 0:
                print("No Records Found for the Topic: " + self.topic)
            else:
                for i, record in enumerate(records):
                    if i >= numOfRecords:
                        break
                    print("key: " + record.key() + "\n" +
                          "value: " + str(record.value()))
        else:
            print("Access to topic is not granted")

    def cont_stream_cmd(self):
        ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
        consumer = ncds_client.ncds_kafka_consumer(
            self.topic) if not self.timestamp else ncds_client.ncds_kafka_consumer(self.topic, self.timestamp)

        try:
            while True:
                message = consumer.poll(sys.maxsize)
                if message is None:
                    print(f"No Records Found for the Topic: {self.topic}")
                else:
                    print(f"value :" + str(message.value()))
                    consumer.commit(message=message, asynchronous=True)

        except KafkaException as e:
            logging.exception(f"Error in cont stream {e.args[0].str()}")
        finally:
            consumer.close()

    def filter_stream_cmd(self):
        symbol_set = None
        msgname_set = None

        if self.symbols is not None:
            symbol_set = set(self.symbols.split(","))

        if self.msgnames is not None:
            msgname_set = set(self.msgnames.split(","))

        ncds_client = NCDSClient(self.security_cfg, self.kafka_cfg)
        consumer = ncds_client.ncds_kafka_consumer(
            self.topic) if not self.timestamp else ncds_client.ncds_kafka_consumer(self.topic, self.timestamp)

        with resources.open_text(sysresources, "consumer-properties.json") as f:
            consumer_props = json.load(f)
        f.close()

        try:
            while True:
                messages = consumer.consume(
                    consumer_props[ConsumerConfig.NUM_MESSAGES], consumer_props[ConsumerConfig.TIMEOUT])
                self.logger.debug(
                    f"number of messages consumed: {len(messages)}")
                if len(messages) == 0:
                    print(f"No Record Found for the Topic: {self.topic}")
                else:
                    for message in messages:
                        symbol = None
                        msg_name = None
                        try:
                            msg_val = message.value()
                            symbol = msg_val['symbol']
                            msg_name = msg_val['schema_name']
                            self.logger.debug(
                                f"{symbol}, msg_name: {msg_name}")
                            if (not self.symbols or symbol in symbol_set) and (
                                    not self.msgnames or msg_name in msgname_set):
                                print(str(message.value()))

                        except KeyError:
                            pass

                        consumer.commit(message=message, asynchronous=True)
        except Exception as e:
            logging.exception(f"Error in filter stream: {e}")

        finally:
            consumer.close()


def load_auth_properties(auth_props_file):
    cfg = {}
    try:
        if auth_props_file:
            with open(auth_props_file) as f:
                cfg = json.load(f)
                f.close()
        else:
            with resources.open_text(configresources, "client-authentication-config.json") as f:
                cfg = json.load(f)
            f.close()

    except OSError as e:
        logging.exception(f"Could not open/read file: {auth_props_file}")
        raise e

    return cfg


def load_kafka_config(kafka_cfg_file):
    cfg = {}
    try:
        if kafka_cfg_file:
            with open(kafka_cfg_file) as f:
                cfg = json.load(f)
            f.close()
        else:
            with resources.open_text(configresources, "kafka-config.json") as f:
                cfg = json.load(f)
            f.close()

    except OSError as e:
        logging.exception(f"Could not open/read file: {kafka_cfg_file}")
        raise e

    return cfg


@click.command()
@click.option("-opt", help="Provide the operation you want to perform")
@click.option("-topic", help="Provide topic for selected option")
@click.option("-symbols", help="Provide topic for selected option")
@click.option("-authprops", help="Provide Client Properties File paths")
@click.option("-kafkaprops", help="Provide Kafka Properties File path")
@click.option("-n", help="Provide number of messages to retrieve", type=int)
@click.option("-msgname", help="Provide name of message based on schema")
@click.option("-msgnames", help="Provide list of message names for selected option")
@click.option("-path", help="Provide the path for key store")
@click.option("-timestamp", help="Provide timestamp in milliseconds", type=int)
def cli(**kwargs):
    session = NCDSSession(kwargs)
    session.main()


if __name__ == "__main__":
    cli()
