from confluent_kafka import DeserializingConsumer
from confluent_kafka.error import (KeyDeserializationError,
                                   ValueDeserializationError)
from confluent_kafka.serialization import (SerializationContext,
                                           MessageField)
import logging


class BasicKafkaConsumer(DeserializingConsumer):
    """
    This is the base class for all Kafka consumers.
    It expands the confluent-kafka Python `DeserializingConsumer <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.DeserializingConsumer>`_ class by adding some utility methods.

    Attributes:
        config (dict): stores dict that stores configuration properties for the confluent-kafka Python `DeserializingConsumer <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#confluent_kafka.DeserializingConsumer>`_
        key_deserializer (Deserializer): deserializer used for message keys
        value_deserializer (func): decode function used to deserialize message values
    """

    def __init__(self, config, key_deserializer, value_deserializer):
        config["key.deserializer"] = key_deserializer
        config["value.deserializer"] = value_deserializer.decode
        self.logger = logging.getLogger(__name__)
        super(BasicKafkaConsumer, self).__init__(config)

    def ensure_assignment(self):
        """
        Ensures that the consumer is assigned,

        Returns:
            a list of TopicPartitions that the consumer has been assigned to
        :rtype: list(`TopicPartitions <https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-topicpartition>`_)
        """
        super(BasicKafkaConsumer, self).poll(0)
        return super(BasicKafkaConsumer, self).assignment()

    def consume(self, num_messages=1, timeout=-1):
        """
        Consume up to the number of messages specified with a timeout for each request

        Args:
            num_messages (int): The maximum number of messages to wait for.
            timeout (float): Maximum time to block waiting for message(Seconds).
        Returns:
            :py:class:`Message` or None on timeout
        Raises:
            KeyDeserializationError: If an error occurs during key deserialization.
            ValueDeserializationError: If an error occurs during value deserialization.
            RuntimeError: if the number of messages is less than 1
        """
        if num_messages < 1:
            raise RuntimeError(
                "The maximum number of messages must be greater than or equal to 1.")

        messages = super(DeserializingConsumer, self).consume(
            num_messages, timeout)

        if messages is None:
            return []

        deserialized_messages = []

        for message in messages:
            deserialized_messages.append(
                self._parse_deserialize_message(message))

        return deserialized_messages

    def _parse_deserialize_message(self, message):
        """
        Internal class method for deserializing and maintaining consistency between poll and consume classes.
        This function will take in a raw serialized message (from cimpl) and return a deserialized message back.

        Args:
            message (cimpl.Message): The serialized message returned from the base consumer class.
        Returns:
            :py:class:`Message` on sucessful deserialization
        Raises:
            KeyDeserializationError: If an error occurs during key deserialization.
            ValueDeserializationError: If an error occurs during value deserialization.
        """
        ctx = SerializationContext(message.topic(), MessageField.VALUE)
        value = message.value()
        if self._value_deserializer is not None:
            try:
                value = self._value_deserializer(value, ctx)
            except Exception as se:
                raise ValueDeserializationError(
                    exception=se, kafka_message=message)

        key = message.key()
        ctx.field = MessageField.KEY
        if self._key_deserializer is not None:
            try:
                key = self._key_deserializer(key, ctx)
            except Exception as se:
                raise KeyDeserializationError(
                    exception=se, kafka_message=message)

        message.set_key(key)
        message.set_value(value)
        return message
