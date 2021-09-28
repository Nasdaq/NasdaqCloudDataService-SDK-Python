import json
import avro
import logging
from importlib import resources
from ncdssdk.src.main.python.ncdsclient.internal.utils import IsItPyTest, SeekToMidnight
from ncdssdk.src.main.python.ncdsclient.internal.utils.AuthenticationConfigLoader import AuthenticationConfigLoader
from ncdssdk.src.main.python.ncdsclient.internal.utils.KafkaConfigLoader import KafkaConfigLoader
import ncdssdk.src.main.resources as sysresources
import ncdssdk.src.main.resources.schemas as schemas
from ncdssdk.src.main.python.ncdsclient.internal.KafkaAvroConsumer import KafkaAvroConsumer
from confluent_kafka import TopicPartition
import ncdssdk.src.main.python.ncdsclient.internal.utils.ConsumerConfig as config
from confluent_kafka import OFFSET_BEGINNING


class ReadSchemaTopic:
    """
    Class to Retrieve the Kafka Schema for the given Topic/Stream.

    Attributes:
        control_schema_name (str): "control" by default
        security_props (dict): properties to be passed in to the AuthenticationConfigLoader
        kafka_props (dict): properties to be passed in to the AuthenticationConfigLoader
        consumer_props (dict): a JSON dict from a user-editable file containing the num_messages and timeout parameters to be passed into a KafkaConsumer's `.consume()` function
    """

    def __init__(self):
        self.control_schema_name = "control"
        self.security_props = None
        self.kafka_props = {}
        self.logger = logging.getLogger(__name__)

        with resources.open_text(sysresources, "consumer-properties.json") as f:
            self.consumer_props = json.load(f)
        f.close()

        self.num_messages = self.consumer_props[config.NUM_MESSAGES]
        self.timeout = self.consumer_props[config.TIMEOUT]

    def read_schema(self, topic):
        auth_config_loader = AuthenticationConfigLoader()
        schema_consumer = self.get_consumer(
            "Control-" + auth_config_loader.get_client_id(self.security_props))
        latest_record = None
        while True:
            schema_messages = schema_consumer.consume(
                self.num_messages, self.timeout)
            if not schema_messages:
                break
            for message in reversed(schema_messages):
                try:
                    msg_val = message.value()

                    latest_record = None
                    if "name" in msg_val and msg_val["name"] == topic:
                        latest_record = message
                    if latest_record and 'schema' in msg_val:
                        break
                except Exception as e:
                    print("Error: ", e)
                    logging.warning(
                        "Message could not be parsed in ReadSchemaTopic.read_schema()")

        message_schema = None
       # print("schema consumer", schema_consumer)
        if latest_record:
            latest_record_val = latest_record.value()
            message_schema = avro.schema.parse(latest_record_val['schema'])
        schema_consumer.close()

        if not message_schema:
            print("WARNING: Using the Old Schema! It might not be the latest schema.")
            message_schema = self.internal_schema(topic)

        self.logger.debug("Returning message schema in read_schema")

        return message_schema

    def set_security_props(self, props):
        self.security_props = props

    def set_kafka_props(self, props):
        for key, val in props.items():
            self.kafka_props[key] = val

    def get_topics(self):
        auth_config_loader = AuthenticationConfigLoader()
        topics = set()
        schema_consumer = self.get_consumer(
            auth_config_loader.get_client_id(self.security_props))

        while True:
            message = schema_consumer.poll(5.0)
            if message is None:
                break

            msg_val = message.value()

            name = msg_val['name']
            topics.add(name)

        schema_consumer.close()
        return topics

    def get_consumer(self, client_id):
        ctrl_msg_str = resources.read_text(
            sysresources, 'ControlMessageSchema.avsc')
        ctrl_msg_schema = avro.schema.parse(ctrl_msg_str)

        if IsItPyTest.is_py_test():
            self.kafka_props = KafkaConfigLoader.load_test_config()

        self.kafka_props[config.AUTO_OFFSET_RESET_CONFIG] = 'earliest'
        self.kafka_props[config.GROUP_ID_CONFIG] = f'{client_id}1'

        kafka_avro_consumer = KafkaAvroConsumer(
            self.kafka_props, ctrl_msg_schema)

        topic_partition = TopicPartition(
            self.control_schema_name, partition=0, offset=OFFSET_BEGINNING)

        kafka_avro_consumer.assign([topic_partition])

        return SeekToMidnight.seek_to_midnight_at_past_day(kafka_avro_consumer, topic_partition, 7)

    def internal_schema(self, topic):
        try:
            topic_schema_str = resources.read_text(schemas, f'{topic}.avsc')
            topic_schema = avro.schema.parse(topic_schema_str)
            return topic_schema
        except Exception as e:
            raise Exception(f"SCHEMA NOT FOUND FOR TOPIC: {topic}")
