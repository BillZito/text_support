"""
`app.py` is where we create our Flask application.
"""

# pylint: disable=import-error, invalid-name

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import DevelopmentConfig, TestConfig, ProductionConfig
from .views import app_views

# Create the flask application.
app = Flask(__name__)

# Given the appropriate environment, set the configuration.
config_options = {
    "DEVELOPMENT": DevelopmentConfig,
    "TEST": TestConfig,
    "PRODUCTION": ProductionConfig
}
config_object = config_options[os.environ["ENVIRONMENT"]]
app.config.from_object(config_object)

# Connect to the database. Other files can use this through importing
# `db` from `.app`.
db = SQLAlchemy(app)

# Instruct flask application to use views defined in `views.py`.
app.register_blueprint(app_views)
