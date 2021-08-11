from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import logging


class Oauth:
    """
    Utility class for creating the oauth callback function passed into the consumer.
    """

    def __init__(self, auth_config):
        self.token_url = auth_config["oauth.token.endpoint.uri"]
        self.client_id = auth_config["oauth.client.id"]
        self.client_secret = auth_config["oauth.client.secret"]
        self.logger = logging.getLogger(__name__)

    def oauth_cb(self, config_str):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        token_json = oauth.fetch_token(
            token_url=self.token_url, client_id=self.client_id, client_secret=self.client_secret)
        token = token_json["access_token"]
        expires_at = token_json["expires_at"]
        return (token, expires_at)
