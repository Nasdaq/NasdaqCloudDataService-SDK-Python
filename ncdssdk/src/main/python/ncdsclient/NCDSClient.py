import logging
from importlib import resources
from ncdssdk.src.main.python.ncdsclient.internal.utils import ConsumerConfig
from ncdssdk.src.main.python.ncdsclient.internal.utils.AuthenticationConfigLoader import AuthenticationConfigLoader
from ncdssdk.src.main.python.ncdsclient.consumer.NasdaqKafkaAvroConsumer import NasdaqKafkaAvroConsumer
from ncdssdk.src.main.python.ncdsclient.internal.utils import IsItPyTest
import ncdssdk.src.main.resources as sysresources
import json
from confluent_kafka import OFFSET_END
from ncdssdk.src.main.python.ncdsclient.internal.utils import LoggingConfig


class NCDSClient:
    """
    This is a client class to access Nasdaq's market data.
    Internal methods are used by NCDSSession to get topics, schemas, messages, and consumer info.

    Attributes:
        security_cfg (dict): Authentication security configuration passed from the client
        kafka_cfg (dict): Kafka consume configuration settings passed in from the client
    """

    def __init__(self, security_cfg, kafka_cfg):
        """
        This method creates a :class:`.NasdaqKafkaAvroConsumer` instance using the configuration info.
        """
        self.nasdaq_kafka_avro_consumer = None
        LoggingConfig.create_logger()
        self.logger = logging.getLogger(__name__)

        if kafka_cfg:
            kafka_cfg['logger'] = logging.getLogger(__name__)

        with resources.open_text(sysresources, "consumer-properties.json") as f:
            self.consumer_props = json.load(f)
        f.close()

        try:
            auth_config_loader = AuthenticationConfigLoader()
            if security_cfg is not None and auth_config_loader.validate_security_config(security_cfg):
                self.nasdaq_kafka_avro_consumer = NasdaqKafkaAvroConsumer(
                    security_cfg, kafka_cfg)
            elif IsItPyTest.is_py_test():
                self.nasdaq_kafka_avro_consumer = NasdaqKafkaAvroConsumer(
                    None, None)
            else:
                raise Exception("Authentication Config is missing")
        except:
            raise Exception("Authentication Arguments are missing")

    def list_topics_for_client(self):
        """
        Method produces a topics list from the :class:`.NasdaqKafkaAvroConsumer` instance.

        Returns: 
            list: A list of eligible topics/streams for the client
        """
        topics = list(self.nasdaq_kafka_avro_consumer.get_topics())
        return topics

    def get_schema_for_topic(self, topic):
        """
        Method takes in a topic and retrieves the schema from the consumer instance. 

        Args:
            topic (str): the topic/stream name
        Returns:
            str: The Kafka schema name for the given topic
        """
        kafka_schema = self.nasdaq_kafka_avro_consumer.get_schema_for_topic(
            topic)
        kafka_schema = str(kafka_schema)
        return kafka_schema

    def ncds_kafka_consumer(self, topic, timestamp=None):
        """
        Retrieves the apache kafka consumer. If the timestamp is not set, the consumer will
        start consuming at midnight of this day if auto.offset.reset in the kafka_cfg is set to
        earliest. If auto.offset.reset is set to some variation of 'latest', the consumer will
        start consuming at the end offset.

        Args:
            topic (string): Topic/Stream name
            timestamp (int): timestamp in milliseconds since the UNIX epoch
        Returns: 
            :class:`KafkaAvroConsumer` : Nasdaq's market data Kafka consumer

        """
        return self.nasdaq_kafka_avro_consumer.get_kafka_consumer(topic, timestamp)

    def top_messages(self, topic_name, timestamp=None):
        """
        Retrieves messages from the given topic. 

        Args:
            topic_name (string): Topic/Stream name
            timestamp (int): timestamp in milliseconds since the UNIX epoch, optional
        Returns:
            list: A list of messages from the given topic
        """
        self.logger.debug(
            f"Before initializing ncds_kafka_consumer in top_messages")
        kafka_consumer = self.ncds_kafka_consumer(topic_name, timestamp)
        self.logger.debug("kafka_consumer is now trying to consume")
        records = kafka_consumer.consume(
            self.consumer_props[ConsumerConfig.NUM_MESSAGES], self.consumer_props[ConsumerConfig.TIMEOUT])
        return records

    def get_sample_messages(self, topic_name, message_name, all_messages):
        """
        If all_messages is True, prints out all messages with given message name and topic. Otherwise, retrieves the first message from the topic with the given message name.

        Args:
            topic_name (str): name of topic we want to get a sample message for
            message_name (str): name of the message, retrieved from the schema
            all_messages (bool): True if function should query for all sample messages, False if function should query for just one
        Return:
            str: The example message(s)
        """
        kafka_consumer = None
        sample_msg = None
        sample_msgs = []
        found = False

        try:
            kafka_consumer = self.ncds_kafka_consumer(topic_name)

            while not found:
                messages = kafka_consumer.consume(
                    self.consumer_props[ConsumerConfig.NUM_MESSAGES], self.consumer_props[ConsumerConfig.TIMEOUT])
                if not messages or self.end_of_data(kafka_consumer):
                    print(
                        "--------------------------------END of Stream------------------")
                    break
                for message in messages:
                    msg_val = message.value()
                    if "schema_name" in msg_val and msg_val["schema_name"] == message_name:
                        sample_msg = str(msg_val)
                        if all_messages:
                            if sample_msg is not None:
                                if IsItPyTest.is_py_test():
                                    sample_msgs.append(msg_val)
                                print("sample message: ", sample_msg)
                        else:
                            found = True
            kafka_consumer.close()
        except Exception as e:
            logging.exception(e)
            raise Exception

        if IsItPyTest.is_py_test() and all_messages:
            return sample_msgs

        return sample_msg

    def end_of_data(self, consumer):
        """
        Checks if there is a final sequence number for this stream signaling the end of the data.
        Final sequence number is delivered in the stream_completed event.

        Args:
            consumer (:class:`KafkaAvroConsumer`): the :class:`KafkaAvroConsumer`
        Returns:
            bool: True if the end of the data stream has been reached, False otherwise
        """
        topic_partitions = consumer.assignment()  # list of topic partitions
        self.logger.debug(f"topic partitions: {topic_partitions}")
        positions = consumer.position(topic_partitions)
        self.logger.debug(f"positions: {positions}")
        for index in range(len(topic_partitions)):
            end_offset = OFFSET_END
            position = positions[index].offset
            if position != end_offset:
                return False
        return True
