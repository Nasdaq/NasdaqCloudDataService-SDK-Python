from ncdssdk.src.main.python.ncdsclient.internal.utils.AuthenticationConfigLoader import AuthenticationConfigLoader
import copy
import pytest


def test_valid_config():
    auth_config = AuthenticationConfigLoader()
    cfg = {
        "oauth.token.endpoint.uri": "unit-test",
        "oauth.client.id": "unit-test",
        "oauth.client.secret": "test",
        "oauth.username.claim": "test"
    }

    assert auth_config.validate_security_config(cfg)


def test_invalid_config():
    auth_config = AuthenticationConfigLoader()
    cfg = {
        "oauth.token.endpoint.uri": "unit-test",
        "oauth.client.id": "unit-test",
        "oauth.client.secret": "test",
        "oauth.username.claim": "test"
    }

    for c in cfg.keys():
        cfg_copy = copy.deepcopy(cfg)
        cfg_copy.pop(c)

        pytest.raises(Exception)


def test_client_id():
    auth_config = AuthenticationConfigLoader()
    cfg = {
        "oauth.token.endpoint.uri": "unit-test",
        "oauth.client.id": "unit-test",
        "oauth.client.secret": "test",
        "oauth.username.claim": "test"
    }
    assert auth_config.get_client_id(cfg) == "unit-test"
