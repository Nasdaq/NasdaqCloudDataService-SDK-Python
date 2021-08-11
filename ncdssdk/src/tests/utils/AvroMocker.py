#import avro_json_serializer
import random
import string


class AvroMocker:
    def __init__(self, schema, num_of_records):
        self.schema = schema
        self.num_of_records = num_of_records

    def create_message(self):
        fields = self.schema.fields
        record = {}
        for field in fields:
            name = field.name
            field_type = field.type.fullname
            if field_type == "int" or field_type == "long":
                record[name] = random.randint(0, 100000000)
            elif field_type == 'string':
                record[name] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        #serializer = avro_json_serializer.AvroJsonSerializer(self.schema)
        #return serializer.to_json(record)
        return record

    def generate_mock_messages(self):
        records = []
        for i in range(self.num_of_records):
            records.append(self.create_message())

        return records
