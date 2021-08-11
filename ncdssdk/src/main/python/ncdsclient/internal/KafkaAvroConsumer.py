from ncdssdk.src.main.python.ncdsclient.internal.BasicKafkaConsumer import BasicKafkaConsumer
from ncdssdk.src.main.python.ncdsclient.internal.AvroDeserializer import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer


class KafkaAvroConsumer(BasicKafkaConsumer):
    """
    Kafka consumer for Avro messages.
    Expands :class:`.BasicKafkaConsumer` by passing in a key and value deserializer.

    Attributes:
        config (dict): dict that stores configuration properties for the `DeserializingConsumer <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.DeserializingConsumer>`_
        message_schema (Schema): schema used for decoding in :class:`.AvroDeserializer` class
    """

    def __init__(self, config, message_schema):
        super(KafkaAvroConsumer, self).__init__(
            config, StringDeserializer('utf_8'), AvroDeserializer(message_schema))

    def assign(self, partitions):
        super(KafkaAvroConsumer, self).assign(partitions)
        super(KafkaAvroConsumer, self).ensure_assignment()
