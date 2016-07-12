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

class TestConfig(Config):
    """
    Configuration for testing mode.
    """
    TESTING = True

class ProductionConfig(Config):
    """
    Configuration for production mode.
    """
    DEBUG = False
