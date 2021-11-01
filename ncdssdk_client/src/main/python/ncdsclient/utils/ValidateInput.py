import sys
from ncdssdk_client.src.main.python.ncdsclient.utils.PrintHelpMessage import print_help_message


class ValidateInput:

    def __init__(self, cmd):
        self.cmd = cmd
        self.test_option = cmd['opt']
        self.topic = cmd['topic']
        self.symbols = cmd['symbols']
        self.msgnames = cmd['msgnames']
        self.message_name = cmd['msgname']
        self.certificate_path = cmd['path']
        self.num_top_messages = cmd['n']
        self.timestamp = cmd['timestamp']

    def validate_user_input(self):
        # check that '-opt' was passed in
        if not self.test_option:
            print("You must provide -opt")
            print_help_message()
            sys.exit()

        if self.test_option == "SCHEMA" or self.test_option == "METRICS":
            if not self.topic:
                print("You must provide -topic")
                print_help_message()
                sys.exit()

        elif self.test_option == "TOP":
            if not self.topic or not self.num_top_messages:
                print(
                    "You must provide -topic and -n (Number of records) for getting top records")
                print_help_message()
                sys.exit()

        elif self.test_option == "GETALLMSGS" or self.test_option == "GETMSG":
            if not self.topic or not self.message_name:
                print("You must provide -topic and -msgname for getting example message")
                print_help_message()
                sys.exit()

        elif self.test_option == "CONTSTREAM":
            if not self.topic:
                print("You must provide -topic")
                print_help_message()
                sys.exit()
            self.topic = self.cmd['topic']

        elif self.test_option == "FILTERSTREAM":
            if not self.topic:
                print("You must provide -topic")
                print_help_message()
                sys.exit()

            if not self.symbols and not self.msgnames:
                print("""You must provide either symbols or msgnames of filtering \n
                    No symbols parsed in -symbols. Ex: -symbols XXX,YYY,ZZZ \n
                    No message names parsed in -msgnames. Ex: -msgnames SeqAdjClosingPrice, SeqDirectoryMessage, SeqEndOfDayTradeSummaryETMF
                """)
                print_help_message()
                sys.exit()
