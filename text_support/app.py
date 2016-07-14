"""
`app.py` is where we create our Flask application.
"""

# pylint: disable=import-error, invalid-name, wrong-import-position

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import environment_config

# Create the flask application.
app = Flask(__name__)

# Given the appropriate environment, set the configuration.
app.config.from_object(environment_config())

# Connect to the database. Other files can use this through importing
# `db` from `.app`.
db = SQLAlchemy(app)

# We import the `views` here, because they rely on the models, which need `db`
# to be defined.
from .views import static_views, webhook_views

# Instruct flask application to use views defined in `views.py`.
app.register_blueprint(static_views)
app.register_blueprint(webhook_views)
