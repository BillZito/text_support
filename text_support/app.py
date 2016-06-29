"""
`app.py` is where we create our Flask application.
"""

# pylint: disable=import-error, invalid-name

from flask import Flask

from .views import app_views

# Create the flask application and instruct it to use all of the views (routes
# with associated functions) defined in `app_views` in `views.py`.
app = Flask(__name__)
app.register_blueprint(app_views)
