import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter, BinaryEncoder
import io


class AvroSerializer():

    def __init__(self, schema):
        self.schema = schema

    def encode(self, record, ctx):
        writer = DatumWriter(self.schema)
        message_bytes = io.BytesIO()
        encoder = BinaryEncoder(message_bytes)

        writer.write(record, encoder)
        return message_bytes.getvalue()
