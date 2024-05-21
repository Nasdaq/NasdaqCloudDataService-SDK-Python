# Nasdaq Data Link

Nasdaq Data Link provides a modern and efficient method of delivery for realtime exchange data and other financial information. Data is made available through a suite of APIs, allowing for effortless integration of data from disparate sources, and a dramatic reduction in time to market for customer-designed applications. The API is highly scalable, and robust enough to support the delivery of real-time exchange data.  

# Products Currently Available
### Equities
#### The Nasdaq Stock Market
- [Nasdaq Basic](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NasdaqBasic-Cloud.pdf) (real-time & delayed)
- [Nasdaq Last Sale+](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NLSPlus-cloud.pdf) (real-time & delayed)
- [Nasdaq TotalView](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/Totalview-ITCH-cloud.pdf)
- [Nasdaq Consolidated Quotes and Trades](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/CQT-cloud.pdf) (real-time & delayed)
#### Nasdaq BX
- [BX BBO](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BX_BBO_Cloud.pdf)
- [BX Last Sale](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BLS_Cloud.pdf)
#### Nasdaq PSX
- [PSX BBO](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PSX_BBO_Cloud.pdf)
- [PSX Last Sale](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PLS_Cloud.pdf)
#### Nasdaq Canada
- [Nasdaq Canada Basic](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/Nasdaq-Basic-Canada-Cloud-Specification.pdf)
#### OTC Markets
- [OTC Markets](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/OTCM-cloud.pdf) (real-time & delayed)
### Indexes & ETPs
- [Global Index Data Service](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/GIDS_Cloud.pdf)
### Options
#### Nasdaq U.S. Derivatives
- [Nasdaq Smart Options](http://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NCDSSmartOptions.pdf)
- [Nasdaq Options Greeks and Implied Volatility](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/GreeksandVols_Specification.pdf)
### Mutual Funds
- [Nasdaq Fund Network](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NFNDS_NCDS.pdf)
### News
- [Financial News](http://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/MTNewswires-cloud.pdf)

# Items To Note

* Connecting to the API requires credentials, which are provided by the Nasdaq Data Operations team during an on-boarding process
* This sample code only connects to one topic (NLSCTA); during on-boarding process, you will receive a topic list that you're entitled to.
* See https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Java for our officially support Java-based SDK.


# Table of Contents
 - [Getting Started](#getting-started)
 - [Using the SDK](#using-the-sdk)

## Getting Started
### Python version support
The SDK currently supports Python 3.9 and above

### Get the SDK
The source code is currently hosted on GitHub at: https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python
- Clone the repository: ```git clone https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python.git```
- Move into the directory ```cd NasdaqCloudDataService-SDK-Python```
- Install the library and its dependencies from local source with ```pip install -e .```

Optional: to use the Jupyter notebook provided, 
- Download Jupyter notebook using either pip ```pip3 install notebook``` or conda ```conda install -c conda-forge notebook```
- To run the notebook, use the command ```jupyter notebook``` and the Notebook Dashboard will open in your browser
- Select the file ```python_sdk_examples.ipynb```

### Stream configuration

Replace example stream properties in the file **kafka-config.json** (https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python/blob/master/ncdssdk_client/src/main/python/resources/kafka-config.json) with provided values during on-boarding.

  Required kafka configuration

```properties
"bootstrap.servers": {streams_endpoint_url}:9094
```

  For optional consumer configurations see: https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md

### Client Authentication configuration

Replace example client authentication properties in the file **client-authentication-config.json** (https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python/blob/master/ncdssdk_client/src/main/python/resources/client-authentication-config.json) with valid credentials provided during on-boarding.

```properties
oauth.token.endpoint.uri: "https://{auth_endpoint_url}/auth/realms/pro-realm/protocol/openid-connect/token"
oauth.client.id: "client_id"
oauth.client.secret: "client_secret"
```

### Logging Configuration

To enable debug logging, edit the file (https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python/blob/master/ncdssdk/src/main/resources/logging.json)
and change the logging levels in whichever handler you would like output to go to. 

For example, to enable debug logging to a file:
```json
"file_handler": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "filename": "logging.log",
      "maxBytes": 10485760,
      "backupCount": 20,
      "encoding": "utf8"
    }
  },

  "loggers": {
    "": {
      "level": "DEBUG",
      "handlers": ["console", "file_handler"],
      "propogate": false
    }
  }
}
```

Next, add a debug option to your kafka configurations:
```python
kafka_cfg = {
    "bootstrap.servers": "{streams_endpoint_url}:9094",
    "auto.offset.reset": "earliest",
    "debug": "all"
}
```


### Create NCDS Session Client

  How to run:
```
-opt -- Provide the operation you want to perform \n" +
  "        * TOP - View the top nnn records in the Topic/Stream\n" +
  "        * SCHEMA - Display the Schema for the topic\n" +
  "        * METRICS - Display the Metrics for the topic\n" +
  "        * TOPICS - List of streams available on Nasdaq Cloud DataService\n" +
  "        * GETMSG - Get one example message for the given message name\n" +
  "        * CONTSTREAM   - Retrieve continuous stream  \n" +
  "        * FILTERSTREAM  - Retrieve continuous stream filtered by symbols and/or msgtypes \n" +
  "        * HELP - help \n" +
"-topic -- Provide topic for selected option         --- REQUIRED for TOP,SCHEMA,METRICS,GETMSG,CONTSTREAM and FILTERSTREAM \n" +
"-symbols -- Provide symbols comma separated list    --- OPTIONAL for FILTERSTREAM" +
"-msgnames -- Provide msgnames comma separated list  --- OPTIONAL for FILTERSTREAM" +
"-authprops -- Provide Client Properties File path   --- For using different set of Client Authentication Properties \n" +
"-kafkaprops -- Provide Kafka Properties File path   --- For using different set of Kafka Properties \n" +
"-n -- Provide number of messages to retrieve        --- REQUIRED for TOP \n" +
"-msgName -- Provide name of message based on schema --- REQUIRED for GETMSG \n" +
"-timestamp -- Provide timestamp in milliseconds     --- OPTIONAL for TOP, CONTSTREAM and FILTERSTREAM\n"
```

A few examples:

Get first 100 records for given stream

```python3.9 ncdssdk_client/src/main/python/ncdsclient/NCDSSession.py -opt TOP -n 100 -topic NLSCTA```

Get all available streams

```python3.9 ncdssdk_client/src/main/python/ncdsclient/NCDSSession.py -opt TOPICS```

## Using the SDK

Below are several examples for how to access data using the SDK. A Jupyter notebook with this same code and information is provided in the file ```python_sdk_examples.ipnyb```

To run these examples, you will need the import and configuration dictionaries below. Replace the config information with your credentials. 

```python
from ncdssdk import NCDSClient

security_cfg = {
    "oauth.token.endpoint.uri": "https://{auth_endpoint_url}/auth/realms/demo/protocol/openid-connect/token",
    "oauth.client.id": "client",
    "oauth.client.secret": "client-secret"
}
kafka_cfg = {
    "bootstrap.servers": "{streams_endpoint_url}:9094",
    "auto.offset.reset": "earliest"
}
```
 
  ### Getting list of data stream available
  List all available data stream for the user

  ```python
  ncds_client = NCDSClient(security_cfg, kafka_cfg)
  topics = ncds_client.list_topics_for_client()
  print("Data set topics:")
  for topic_entry in topics:
  print(topic_entry)
  ```

  Example output:
  ```
  List of streams available on Nasdaq Cloud Data Service:
  GIDS
  NLSUTP
  NLSCTA
  ```

  ### Getting schema for the stream
  This method returns the schema for the stream in Apache Avro format (https://avro.apache.org/docs/current/spec.html)
  ```python
  ncds_client = NCDSClient(security_cfg, kafka_cfg)
  topic = "NLSCTA"
  schema = ncds_client.get_schema_for_topic(topic)
  print(schema)
  ```

  Example output:
  ```
  [ {
  "type" : "record",
  "name" : "SeqAdjClosingPrice",
  "namespace" : "com.nasdaq.equities.trades.applications.nls.messaging.binary21",
  "fields" : [ {
    "name" : "SoupPartition",
    "type" : "int"
  }, {
    "name" : "SoupSequence",
    "type" : "long"
  }, {
    "name" : "trackingID",
    "type" : "long"
  }, {
    "name" : "msgType",
    "type" : "string"
  }, {
    "name" : "symbol",
    "type" : "string"
  }, {
    "name" : "securityClass",
    "type" : "string"
  }, {
    "name" : "adjClosingPrice",
    "type" : "int"
  } ],
  "version" : "1"
  }, {...
  } .......
  .... ]
  ```
  
  ### Get first 10 messages of the stream 
  ```python
  ncds_client = NCDSClient(security_cfg, kafka_cfg)
  topic = "NLSCTA"
  records = ncds_client.top_messages(topic)
  for i in range(0, 10):
      print("key: ", records[i].key())
      print("value: ", str(records[i].value()))
  ```
  Example output:
  ```
  Top 10 Records for the Topic: NLSCTA
key: 14600739
value: {"SoupPartition": 0, "SoupSequence": 14600739, "trackingID": 72000000024569, "msgType": "S", "event": "E", "schema_name": "SeqSystemEventMessage"}
key: 14600740
value: {"SoupPartition": 0, "SoupSequence": 14600740, "trackingID": 72900000006514, "msgType": "J", "symbol": "A", "securityClass": "N", "consHigh": 1487799, "consLow": 1466600, "consClose": 1478100, "cosolidatedVolume": 1259303, "consOpen": 1486800, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600741
value: {"SoupPartition": 0, "SoupSequence": 14600741, "trackingID": 72900000006514, "msgType": "J", "symbol": "AA", "securityClass": "N", "consHigh": 378039, "consLow": 366800, "consClose": 368400, "cosolidatedVolume": 6047752, "consOpen": 372000, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600742
value: {"SoupPartition": 0, "SoupSequence": 14600742, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAA", "securityClass": "P", "consHigh": 250400, "consLow": 250101, "consClose": 250250, "cosolidatedVolume": 3121, "consOpen": 250400, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600743
value: {"SoupPartition": 0, "SoupSequence": 14600743, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAAU", "securityClass": "P", "consHigh": 176500, "consLow": 174700, "consClose": 176000, "cosolidatedVolume": 303143, "consOpen": 175000, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600744
value: {"SoupPartition": 0, "SoupSequence": 14600744, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAC", "securityClass": "N", "consHigh": 97900, "consLow": 97500, "consClose": 97500, "cosolidatedVolume": 19787, "consOpen": 97600, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600745
value: {"SoupPartition": 0, "SoupSequence": 14600745, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAC+", "securityClass": "N", "consHigh": 12800, "consLow": 12000, "consClose": 12500, "cosolidatedVolume": 85652, "consOpen": 12300, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600746
value: {"SoupPartition": 0, "SoupSequence": 14600746, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAC=", "securityClass": "N", "consHigh": 100500, "consLow": 99500, "consClose": 100000, "cosolidatedVolume": 74060, "consOpen": 99500, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600747
value: {"SoupPartition": 0, "SoupSequence": 14600747, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAIC", "securityClass": "N", "consHigh": 41850, "consLow": 40600, "consClose": 40600, "cosolidatedVolume": 241597, "consOpen": 41800, "schema_name": "SeqEndOfDayTradeSummary"}
key: 14600748
value: {"SoupPartition": 0, "SoupSequence": 14600748, "trackingID": 72900000006514, "msgType": "J", "symbol": "AAIC-B", "securityClass": "N", "consHigh": 249700, "consLow": 249700, "consClose": 249700, "cosolidatedVolume": 238, "consOpen": 249700, "schema_name": "SeqEndOfDayTradeSummary"}
```

### Get first 10 messages of the stream from given timestamp
This returns the first 10 available messages of the stream given timestamp in milliseconds since the UNIX epoch.
```python
ncds_client = NCDSClient(security_cfg, kafka_cfg)
topic="NLSCTA"
timestamp = 1590084446510
records = ncds_client.top_messages(topic, timestamp)
for i in range(0, 10):
    print("key: ", records[i].key())
    print("value: ", str(records[i].value()))
```

Example output:
```
Offset: 105834100
Top 10 Records for the Topic:NLSCTA
key:9362630
value :{"SoupPartition": 0, "SoupSequence": 9362630, "trackingID": 50845551492208, "msgType": "T", "marketCenter": "L", "symbol": "SIVR    ", "securityClass": "P", "controlNumber": "0000A2MLOB", "price": 164797, "size": 1, "saleCondition": "@  o", "cosolidatedVolume": 520174}
key:9362631
value :{"SoupPartition": 0, "SoupSequence": 9362631, "trackingID": 50845557908136, "msgType": "T", "marketCenter": "Q", "symbol": "TJX     ", "securityClass": "N", "controlNumber": "   8358213", "price": 540300, "size": 100, "saleCondition": "@   ", "cosolidatedVolume": 16278768}
key:9362632
value :{"SoupPartition": 0, "SoupSequence": 9362632, "trackingID": 50845565203932, "msgType": "T", "marketCenter": "L", "symbol": "CMI     ", "securityClass": "N", "controlNumber": "0000A2MLOC", "price": 1579900, "size": 100, "saleCondition": "@   ", "cosolidatedVolume": 568622}
key:9362633
value :{"SoupPartition": 0, "SoupSequence": 9362633, "trackingID": 50845565791061, "msgType": "T", "marketCenter": "L", "symbol": "UTI     ", "securityClass": "N", "controlNumber": "0000A2MLOD", "price": 70150, "size": 64, "saleCondition": "@  o", "cosolidatedVolume": 151359}
key:9362634
value :{"SoupPartition": 0, "SoupSequence": 9362634, "trackingID": 50845566628604, "msgType": "T", "marketCenter": "L", "symbol": "UFS     ", "securityClass": "N", "controlNumber": "0000A2MLOE", "price": 203660, "size": 24, "saleCondition": "@  o", "cosolidatedVolume": 664962}
key:9362635
value :{"SoupPartition": 0, "SoupSequence": 9362635, "trackingID": 50845569154140, "msgType": "T", "marketCenter": "L", "symbol": "KR      ", "securityClass": "N", "controlNumber": "0000A2MLOF", "price": 320350, "size": 100, "saleCondition": "@   ", "cosolidatedVolume": 4054473}
key:9362636
value :{"SoupPartition": 0, "SoupSequence": 9362636, "trackingID": 50845577944984, "msgType": "T", "marketCenter": "L", "symbol": "PAGP    ", "securityClass": "N", "controlNumber": "0000A2MLOG", "price": 98350, "size": 100, "saleCondition": "@   ", "cosolidatedVolume": 1557084}
key:9362637
value :{"SoupPartition": 0, "SoupSequence": 9362637, "trackingID": 50845588007117, "msgType": "T", "marketCenter": "L", "symbol": "LUV     ", "securityClass": "N", "controlNumber": "0000A2MLOH", "price": 297413, "size": 4, "saleCondition": "@  o", "cosolidatedVolume": 16791899}
key:9362638
value :{"SoupPartition": 0, "SoupSequence": 9362638, "trackingID": 50845596356365, "msgType": "T", "marketCenter": "L", "symbol": "M       ", "securityClass": "N", "controlNumber": "0000A2MLOI", "price": 54000, "size": 10, "saleCondition": "@  o", "cosolidatedVolume": 39273663}
key:9362639
value :{"SoupPartition": 0, "SoupSequence": 9362639, "trackingID": 50845600594567, "msgType": "T", "marketCenter": "L", "symbol": "TTM     ", "securityClass": "N", "controlNumber": "0000A2MLOJ", "price": 56000, "size": 400, "saleCondition": "@   ", "cosolidatedVolume": 1293244}
```

### Get example message from stream
Print message to the console for given message name.
```python
ncds_client = NCDSClient(security_cfg, kafka_cfg)
topic = "NLSCTA"
print(ncds_client.get_sample_messages(topic, "SeqDirectoryMessage", all_messages=False))
```

Example output:
```
{'SoupPartition': 0, 'SoupSequence': 500, 'trackingID': 11578737109589, 'msgType': 'R', 'symbol': 'AMN', 'marketClass': 'N', 'fsi': '', 'roundLotSize': 100, 'roundLotOnly': 'N', 'issueClass': 'C', 'issueSubtype': 'Z', 'authenticity': 'P', 'shortThreshold': 'N', 'ipo': '', 'luldTier': '2', 'etf': 'N', 'etfFactor': 0, 'inverseETF': 'N', 'compositeId': 'BBG000BCT197', 'schema_name': 'SeqDirectoryMessage'}
```

### Get continuous stream
```python

ncds_client = NCDSClient(security_cfg, kafka_cfg)
topic = "NLSCTA"
consumer = ncds_client.ncds_kafka_consumer(topic)
while True:
    messages = consumer.consume(num_messages=1, timeout=5)
    if len(messages) == 0:
        print(f"No Records Found for the Topic: {topic}")
              
    for message in messages:
        print(f"value :" + str(message.value()))
```

Example output:
*note that only the first ten messages of the stream are shown in this example*
```
value :{"SoupPartition": 0, "SoupSequence": 1, "trackingID": 7233292771056, "msgType": "S", "event": "O", "schema_name": "SeqSystemEventMessage"}
value :{"SoupPartition": 0, "SoupSequence": 2, "trackingID": 11578719526113, "msgType": "R", "symbol": "A", "marketClass": "N", "fsi": "", "roundLotSize": 100, "roundLotOnly": "N", "issueClass": "C", "issueSubtype": "Z", "authenticity": "P", "shortThreshold": "N", "ipo": "", "luldTier": "1", "etf": "N", "etfFactor": 0, "inverseETF": "N", "compositeId": "BBG000C2V3D6", "schema_name": "SeqDirectoryMessage"}
value :{"SoupPartition": 0, "SoupSequence": 3, "trackingID": 11578719526113, "msgType": "G", "symbol": "A", "securityClass": "N", "adjClosingPrice": 1500300, "schema_name": "SeqAdjClosingPrice"}
value :{"SoupPartition": 0, "SoupSequence": 4, "trackingID": 11578719831656, "msgType": "R", "symbol": "AA", "marketClass": "N", "fsi": "", "roundLotSize": 100, "roundLotOnly": "N", "issueClass": "C", "issueSubtype": "Z", "authenticity": "P", "shortThreshold": "N", "ipo": "", "luldTier": "1", "etf": "N", "etfFactor": 1, "inverseETF": "N", "compositeId": "BBG00B3T3HD3", "schema_name": "SeqDirectoryMessage"}
value :{"SoupPartition": 0, "SoupSequence": 5, "trackingID": 11578719831656, "msgType": "G", "symbol": "AA", "securityClass": "N", "adjClosingPrice": 374400, "schema_name": "SeqAdjClosingPrice"}
value :{"SoupPartition": 0, "SoupSequence": 6, "trackingID": 11578719879872, "msgType": "R", "symbol": "AAA", "marketClass": "P", "fsi": "", "roundLotSize": 100, "roundLotOnly": "N", "issueClass": "Q", "issueSubtype": "I", "authenticity": "P", "shortThreshold": "N", "ipo": "", "luldTier": "2", "etf": "Y", "etfFactor": 1, "inverseETF": "N", "compositeId": "BBG00X5FSP48", "schema_name": "SeqDirectoryMessage"}
value :{"SoupPartition": 0, "SoupSequence": 7, "trackingID": 11578719879872, "msgType": "G", "symbol": "AAA", "securityClass": "P", "adjClosingPrice": 250050, "schema_name": "SeqAdjClosingPrice"}
value :{"SoupPartition": 0, "SoupSequence": 8, "trackingID": 11578719916519, "msgType": "R", "symbol": "AAAU", "marketClass": "P", "fsi": "", "roundLotSize": 100, "roundLotOnly": "N", "issueClass": "Q", "issueSubtype": "I", "authenticity": "P", "shortThreshold": "N", "ipo": "", "luldTier": "1", "etf": "Y", "etfFactor": 1, "inverseETF": "N", "compositeId": "BBG00LPXX872", "schema_name": "SeqDirectoryMessage"}
value :{"SoupPartition": 0, "SoupSequence": 9, "trackingID": 11578719916519, "msgType": "G", "symbol": "AAAU", "securityClass": "P", "adjClosingPrice": 179850, "schema_name": "SeqAdjClosingPrice"}
value :{"SoupPartition": 0, "SoupSequence": 10, "trackingID": 11578719950254, "msgType": "R", "symbol": "AAC", "marketClass": "N", "fsi": "", "roundLotSize": 100, "roundLotOnly": "N", "issueClass": "O", "issueSubtype": "Z", "authenticity": "P", "shortThreshold": "N", "ipo": "", "luldTier": "2", "etf": "N", "etfFactor": 1, "inverseETF": "N", "compositeId": "BBG00YZC2Z91", "schema_name": "SeqDirectoryMessage"}
```

### Example syntax to run the client based on this SDK

1. To list streams available on Nasdaq Cloud Data Service

```python3.9 NCDSSession.py -opt TOPICS```

2. To display the schema for the given topic

```python3.9 NCDSSession.py -opt SCHEMA -topic NLSCTA```

3. To dump top n records from the given topic

```python3.9 NCDSSession.py -opt TOP -n 10 -topic NLSCTA```

4. To use client based specific authorization file instead of using from the resources of client code base

```python3.9 NCDSSession.py -opt TOP -n 10 -topic NLSCTA -authprops client-authentication-config.json```

5. To use the specific kafka properties instead of using the kafka properties from the resources of the client base code

```python3.9 NCDSSession.py -opt TOP -n 10 -topic NLSCTA -kafkaprops kafka-config.json```

6. To use the specific client based authorization file and specific kafka properties file

```python3.9 NCDSSession.py -opt TOP -n 10 -topic NLSCTA -authprops client-authentication-config.json -kafkaprops kafka-config.json```

7. To display a specific message type

```python3.9 NCDSSession.py -opt GETMSG -topic NLSCTA -msgname SeqDirectoryMessage```

8. To dump top n records from the given topic from given timestamp in milliseconds since the UNIX epoch

```python3.9 NCDSSession.py -opt TOP -n 10 -topic NLSCTA -timestamp 1590084445610```

9. To retrieve a continuous stream of messages from the given topic

```python3.9 NCDSSession.py -opt CONTSTREAM -topic NLSCTA```

10. To retrieve a stream of messages from the given topic, filtered by symbols or message names

```python3.9 NCDSSession.py -opt FILTERSTREAM -topic NLSCTA -symbols SPCE```

## Documentation

An addition to the example application, there is extra documentation at the package and class level, which are located in project ```https://github.com/Nasdaq/NasdaqCloudDataService-SDK-Python​/tree/master/ncdssdk/docs```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

Code and documentation released under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)
  
