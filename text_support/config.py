"""
`config.py` contains configuration info for our flask application.
"""

# pylint: disable=too-few-public-methods

import os

class Config(object):
    """
    Configuration for flask application.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    """
    Configuration for development mode.
    """
    DEVELOPMENT = True
    ENVIRONMENT = "DEVELOPMENT"

class TestConfig(Config):
    """
    Configuration for testing mode.
    """
    TESTING = True
    ENVIRONMENT = "TEST"

class ProductionConfig(Config):
    """
    Configuration for production mode.
    """
    DEBUG = False
    ENVIRONMENT = "PRODUCTION"

def environment_config():
    """
    Return the configuration for the proper environment.

    Returns:
        Config: The configuration object related to this environment.
    """
    config_options = {
        "DEVELOPMENT": DevelopmentConfig,
        "TEST": TestConfig,
        "PRODUCTION": ProductionConfig
    }
    return config_options[os.environ["ENVIRONMENT"]]
