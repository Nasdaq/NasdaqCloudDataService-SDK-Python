from ncdssdk.src.main.python.ncdsclient.internal.ReadSchemaTopic import ReadSchemaTopic
import avro.schema as schema


def test_internal_schema():
    readSchemaTopic = ReadSchemaTopic()

    schema_file = "../resources/NLSCTA.avsc"
    correct_schema = schema.Parse(open(schema_file, 'r').read())

    test_schema = readSchemaTopic.internal_schema('NLSCTA')

    assert correct_schema == test_schema
