import io
from avro.io import DatumReader, BinaryDecoder
import json
import logging



class AvroDeserializer():
    """
    Decodes the given schema for the user and returns the decoded data.
    Wrapper for the AvroDeserializer.

    Attributes:
        schema (Schema): the schema loaded from a schema file
    """

    def __init__(self, schema):
        self.schema = schema
        self.logger = logging.getLogger(__name__)

    def decode(self, msg_value, ctx):
        reader = DatumReader(self.schema)
        message_bytes = io.BytesIO(msg_value)
        decoder = BinaryDecoder(message_bytes)
        try:
            event_dict = reader.read(decoder)
        except Exception as e:
            logging.exception(e)
            raise e

        union_schema = True
        try:
            #  Get the union index to get the schema and schema name
            schema_message_bytes = io.BytesIO(msg_value)
            schema_decoder = BinaryDecoder(schema_message_bytes)
            schema_index = int(schema_decoder.read_long())
            schema_name = reader.readers_schema.schemas[schema_index].name
        except Exception as e:
            union_schema = False
            pass

        for key in event_dict:
            if type(event_dict[key]) == str:
                event_dict[key] = event_dict[key].strip()

        # Initialize schema name in the message based on type of schema
        if union_schema:
            event_dict["schema_name"] = schema_name
        else:
            event_dict["schema_name"] = reader.readers_schema.name

        return event_dict
