"""
`app.py` is where we create our Flask application.
"""

# pylint: disable=import-error, invalid-name

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import environment_config
from .views import app_views

# Create the flask application.
app = Flask(__name__)

# Given the appropriate environment, set the configuration.
app.config.from_object(environment_config())

# Connect to the database. Other files can use this through importing
# `db` from `.app`.
db = SQLAlchemy(app)

# Instruct flask application to use views defined in `views.py`.
app.register_blueprint(app_views)
