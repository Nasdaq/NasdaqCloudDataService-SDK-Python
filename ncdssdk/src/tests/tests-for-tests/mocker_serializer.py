from ncdssdk.src.tests.utils.AvroSerializer import AvroSerializer
from ncdssdk.src.tests.utils.AvroMocker import AvroMocker
from ncdssdk.src.main.python.ncdsclient.internal.AvroDeserializer import AvroDeserializer
import avro

schema_str = r"""{
  "type" : "record",
  "name" : "SeqEtpIpvValue",
  "namespace" : "com.nasdaq.mdic.mocker",
  "fields" : [ {
    "name" : "SoupPartition",
    "type" : "int"
  }, {
    "name" : "SoupSequence",
    "type" : "long"
  }, {
    "name" : "msgType",
    "type" : "string"
  } ],
  "version" : "1"
}"""

schema = avro.schema.parse(schema_str)
serializer = AvroSerializer(schema)
deserializer = AvroDeserializer(schema)
mocker = AvroMocker(schema, 1)

if __name__ == '__main__':
    record = mocker.create_message()
    print(record)
    encoded_bytes = serializer.encode(record, "")
    print(encoded_bytes)
    deserialized_msg = deserializer.decode(encoded_bytes, "")
    print(deserialized_msg)
