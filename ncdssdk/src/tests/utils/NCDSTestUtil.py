import uuid
import avro
import logging
from importlib import resources
import ncdssdk.src.tests.resources as testresources
from confluent_kafka import SerializingProducer
import time
from ncdssdk.src.tests.utils.AvroMocker import AvroMocker
from ncdssdk.src.tests.utils.AvroSerializer import AvroSerializer


class NCDSTestUtil:
    def __init__(self):
        self.kafka_test_server = None
        self.kafka_test_utils = None
        self.config = {}
        self.topics_on_stream = []
        self.mock_messages_on_stream = []
        self.GIDS_messages_on_stream = []
        self.ctrl_topic = "control"
        self.mock_data_stream = "MOCK.stream"
        self.GIDS_data_stream = "GIDS.stream"
        self.timestamp_to_seek_from = 0

        self.add_schemas_to_control_topic()
        self.push_mock_messages()
        self.push_gids_messages()

    def get_producer_config(self, schema_file):
        msg_str = resources.read_text(
            testresources, schema_file)
        schema = avro.schema.parse(msg_str)
        message_serializer = AvroSerializer(schema)

        kafka_connect_string = "localhost:9092"
        self.config["bootstrap.servers"] = kafka_connect_string
        self.config["client.id"] = uuid.uuid4()
        self.config["request.timeout.ms"] = 15000
        self.config["value.serializer"] = message_serializer.encode

        return self.config

    def add_schemas_to_control_topic(self):
        try:
            # define our topics
            nls_key = "NLSUTP"
            gids_key = "GIDS"
            mock_key = "Mock"

            all_topics = [nls_key, gids_key, mock_key]

            all_records = []

            ctrl_schema_file = 'ControlMessageSchema.avsc'
            ctrl_msg_str = resources.read_text(testresources, ctrl_schema_file)
            ctrl_schema = avro.schema.parse(ctrl_msg_str)
            mocker = AvroMocker(ctrl_schema.schemas[1], 1)

            for topic in all_topics:
                topic_string = "test"+topic+".avsc"
                msg_str = resources.read_text(
                    testresources, topic_string)
                record = mocker.create_message()
                record["schema"] = str(msg_str)
                record["name"] = topic.upper()
                all_records.append(record)
                self.topics_on_stream.append(topic)

            # creating producer
            producer_config = self.get_producer_config(ctrl_schema_file)

            try:
                producer = SerializingProducer(producer_config)

                for record in all_records:
                    producer.produce(
                        self.ctrl_topic, value=record)

                producer.flush()

                # close producer
            except Exception as e:
                logging.exception(e)

        except Exception as e:
            logging.exception(e)

    def get_added_topics(self):
        return self.topics_on_stream

    def get_mock_messages(self):
        return self.mock_messages_on_stream

    def get_GIDS_messages(self):
        return self.GIDS_messages_on_stream

    def get_schema_for_topic(self, schema_file):
        schema_msg_str = resources.read_text(testresources, schema_file)
        return avro.schema.parse(schema_msg_str)

    def on_delivery(self, err, msg):
        if (msg.offset() == 2):
            self.timestamp_to_seek_from = msg.timestamp()[1]

    def push_mock_messages(self):
        records = self.get_mocker_generic_record(10)
        mock_schema_file = 'testMock.avsc'
        producer_config = self.get_producer_config(mock_schema_file)
        try:
            # create producer
            mocker_producer = SerializingProducer(producer_config)

            # add mock records to topic
            for record in records:
                self.mock_messages_on_stream.append(record)
                mocker_producer.produce(
                    self.mock_data_stream, value=record, on_delivery=self.on_delivery)
                time.sleep(1)
                mocker_producer.flush()

        except Exception as e:
            logging.exception(e)

    def get_mocker_generic_record(self, number_of_records):
        mock_msg_str = resources.read_text(testresources, 'testMock.avsc')
        mocker_schema = avro.schema.parse(mock_msg_str)

        avro_mocker = AvroMocker(mocker_schema, number_of_records)
        return avro_mocker.generate_mock_messages()

    def push_gids_messages(self):
        records = self.get_GIDS_generic_record(5)
        GIDS_schema_file = 'testGIDS.avsc'
        producer_config = self.get_producer_config(GIDS_schema_file)
        try:
            # create producer
            GIDS_producer = SerializingProducer(producer_config)
            # add GIDS records to topic
            for record in records:
                self.GIDS_messages_on_stream.append(record)
                GIDS_producer.produce(self.GIDS_data_stream, value=record)

            GIDS_producer.flush()

        except Exception as e:
            logging.exception(e)

    def get_GIDS_generic_record(self, number_of_records):
        mock_msg_str = resources.read_text(testresources, 'testGIDS.avsc')
        GIDS_schema = avro.schema.parse(mock_msg_str)

        avro_mocker = AvroMocker(GIDS_schema.schemas[0], number_of_records)
        avro_mocker2 = AvroMocker(GIDS_schema.schemas[3], number_of_records)

        commodities_msgs = avro_mocker.generate_mock_messages()
        equities_msgs = avro_mocker2.generate_mock_messages()

        GIDS_messages = commodities_msgs + equities_msgs

        return GIDS_messages
