import logging.config
from ncdssdk.src.main import resources as sysresources
from importlib import resources
import json

def create_logger():
    with resources.open_text(sysresources, "logging.json") as f:
        config = json.load(f)

    logging.config.dictConfig(config)