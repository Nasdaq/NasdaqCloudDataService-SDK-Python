import os
from ncdssdk.src.main.python.ncdsclient.internal.utils.IsItPyTest import is_py_test
from ncdssdk.src.main.python.ncdsclient.internal.utils.Oauth import Oauth
import logging


class AuthenticationConfigLoader:
    """
    Utility to load the auth configuration parameters.
    """

    def __init__(self):
        self.OAUTH_TOKEN_ENDPOINT_URI = "oauth.token.endpoint.uri"
        self.OAUTH_CLIENT_ID = "oauth.client.id"
        self.OAUTH_CLIENT_SECRET = "oauth.client.secret"
        self.OAUTH_USERNAME_CLAIM = "oauth.username.claim"
        self.logger = logging.getLogger(__name__)

    def get_client_id(self, cfg):
        try:
            if not cfg:
                raise Exception("Missing config.")
            if not is_py_test():
                clientID = cfg[self.OAUTH_CLIENT_ID] if not os.getenv(
                    "OAUTH_CLIENT_ID") else os.getenv("OAUTH_CLIENT_ID")
            else:
                clientID = "unit-test"
            return clientID
        except Exception as e:
            logging.exception(e)
            return

    def add_nasdaq_specific_auth_properties(self, properties):
        if not is_py_test():
            properties["oauth.username.claim"] = "preferred_username"

        return properties

    def validate_security_config(self, cfg):
        self.add_nasdaq_specific_auth_properties(cfg)
        if self.OAUTH_TOKEN_ENDPOINT_URI not in cfg or cfg[self.OAUTH_TOKEN_ENDPOINT_URI] is None:
            raise Exception("Authentication Setting :" +
                            self.OAUTH_TOKEN_ENDPOINT_URI + " Missing")
        if self.OAUTH_CLIENT_ID not in cfg or cfg[self.OAUTH_CLIENT_ID] is None and os.getenv("OAUTH_CLIENT_ID") is None:
            raise Exception("Authentication Setting :" +
                            self.OAUTH_CLIENT_ID + " Missing")
        if self.OAUTH_CLIENT_SECRET not in cfg or cfg[self.OAUTH_CLIENT_SECRET] is None and os.getenv("OAUTH_CLIENT_SECRET") is None:
            raise Exception("Authentication Setting :" +
                            self.OAUTH_CLIENT_SECRET + " Missing")
        if self.OAUTH_USERNAME_CLAIM not in cfg or cfg[self.OAUTH_USERNAME_CLAIM] is None and os.getenv("OAUTH_USERNAME_CLAIM") is None:
            raise Exception("Authentication Setting :" +
                            self.OAUTH_USERNAME_CLAIM + " Missing")
        return True
