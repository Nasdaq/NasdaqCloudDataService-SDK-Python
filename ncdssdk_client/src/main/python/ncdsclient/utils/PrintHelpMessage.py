def print_help_message():
    print("-opt -- Provide the operation you want to perform \n" +
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
          )
