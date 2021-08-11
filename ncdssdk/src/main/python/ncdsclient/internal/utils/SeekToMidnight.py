import logging
import sys
from confluent_kafka import OFFSET_BEGINNING, OFFSET_INVALID
from datetime import datetime, date, timedelta, time

logger = logging.getLogger(__name__)


def seek_to_midnight_at_past_day(kafka_avro_consumer, topic_partition, num_days_ago=0):
    topic_partition.offset = get_timestamp_at_midnight(num_days_ago)
    logger.debug(
        f"Num days ago: {num_days_ago}. Setting partition offset to timestamp: {topic_partition.offset}")
    try:
        logger.debug(f"topic partition: {topic_partition}")
        offsets_for_times = kafka_avro_consumer.offsets_for_times(
            [topic_partition], timeout=5)
    except Exception as e:
        logger.exception(e)
        sys.exit(0)
    logger.debug(f"{offsets_for_times[0]}: offsets for times")
    partition_offset = offsets_for_times[0].offset
    if offsets_for_times and partition_offset is not OFFSET_INVALID:
        topic_partition.offset = partition_offset
        logger.debug(f"Seeking to topic partition: {topic_partition}")
        logger.debug(
            f"making sure partition is assigned before seeking: {kafka_avro_consumer.ensure_assignment()}")
        kafka_avro_consumer.seek(topic_partition)
    else:
        topic_partition.offset = OFFSET_BEGINNING
        logger.debug(
            f"No available offset. Continuing to seek from OFFSET_BEGINNING: {topic_partition}")
        kafka_avro_consumer.seek(topic_partition)
    return kafka_avro_consumer


def get_timestamp_at_midnight(num_days_ago=0):
    past_day = date.today()-timedelta(days=num_days_ago)
    midnight = datetime.combine(past_day, time.min)
    return int(midnight.timestamp() * 1000)
