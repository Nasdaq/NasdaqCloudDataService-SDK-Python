from ncdssdk.src.tests.utils.NCDSTestUtil import NCDSTestUtil
from ncdssdk import NCDSClient
import json
import pytest


ncds_test_util = NCDSTestUtil()


def test_NCDS_client():
    ncds_client = NCDSClient(None, None)
    assert ncds_client is not None


def test_list_topics_for_the_client():
    ncds_client = NCDSClient(None, None)
    topics = ncds_client.list_topics_for_client()
    added_topics = ncds_test_util.get_added_topics()
    assert topics.sort() == added_topics.sort()


def test_get_schema_for_the_topic():
    ncds_client = NCDSClient(None, None)
    topic = "GIDS"
    schema_from_sdk = ncds_client.get_schema_for_topic(topic)
    schema_file = "testGIDS.avsc"
    schema_from_file = ncds_test_util.get_schema_for_topic(schema_file)
    assert schema_from_sdk == schema_from_file


def test_top_messages_with_timestamp():
    topic = "MOCK"
    mock_records = ncds_test_util.get_mock_messages()
    for mock_record in mock_records:
        mock_record["schema_name"] = "SeqEtpIpvValue"
    mock_records_from_kafka = []
    timestamp = ncds_test_util.timestamp_to_seek_from
    ncds_client = NCDSClient(None, None)
    records = ncds_client.top_messages(topic, timestamp)
    for record in records:
        print(record.offset(), record.timestamp())
        mock_records_from_kafka.append(record.value())
    assert len(mock_records_from_kafka) == 8
    assert mock_records[2:] == mock_records_from_kafka


def test_insertion():
    mock_records = ncds_test_util.get_mock_messages()
    for mock_record in mock_records:
        mock_record["schema_name"] = "SeqEtpIpvValue"
    mock_records_from_kafka = []
    topic = "MOCK"
    ncds_client = NCDSClient(None, None)
    records = ncds_client.top_messages(topic)
    for record in records:
        mock_records_from_kafka.append(record.value())
    assert mock_records == mock_records_from_kafka


def test_get_sample_message():
    mock_records = ncds_test_util.get_mock_messages()
    mock_msg = mock_records[-1]
    mock_msg["schema_name"] = "SeqEtpIpvValue"

    topic = "MOCK"
    msg_name = "SeqEtpIpvValue"
    ncds_client = NCDSClient(None, None)
    record = ncds_client.get_sample_messages(topic, msg_name, False)

    assert str(mock_msg) == record


def test_get_all_sample_messages():
    GIDS_records = ncds_test_util.get_GIDS_messages()
    for i, record in enumerate(GIDS_records):
        if i < 5:
            record["schema_name"] = "SeqEquitiesSummary"
        else:
            record["schema_name"] = "SeqEtpIpvValue"
    topic = "GIDS"
    msg_name = "SeqEtpIpvValue"
    ncds_client = NCDSClient(None, None)
    records = ncds_client.get_sample_messages(topic, msg_name, True)
    print("mock records: ", GIDS_records)
    print("records from ncdsclient: ", records)
    assert len(records) == 5
    assert GIDS_records[5:] == records


def test_get_sample_message_incorrect_topic():
    mock_records = ncds_test_util.get_mock_messages()
    mock_msg = mock_records[0]
    mock_msg["schema_name"] = "SeqEtpIpvValue"

    topic = "MUCK"
    msg_name = "SeqEtpIpvValue"
    ncds_client = NCDSClient(None, None)

    with pytest.raises(Exception):
        ncds_client.get_sample_messages(topic, msg_name, False)


def test_get_schema_for_the_incorrect_topic():
    ncds_client = NCDSClient(None, None)
    topic = "MOCK"
    schema_from_sdk = ncds_client.get_schema_for_topic(topic)
    schema_file = "testGIDS.avsc"
    schema_from_file = ncds_test_util.get_schema_for_topic(schema_file)
    assert schema_from_sdk != schema_from_file

    # with pytest.raises(Exception):
    #     schema_from_file = ncds_test_util.get_schema_for_topic(schema_file)
