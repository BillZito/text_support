"""
`views.py` is where we define the routes of this application.
"""

# pylint: disable=import-error, invalid-name

from flask import Blueprint

# We define `app_views` as a Blueprint so that we can import the views in
# `app.py`. This allows all of the `view` logic to be stored in a single file.
# Read more [here](http://flask.pocoo.org/docs/0.11/blueprints/).
app_views = Blueprint('app_views', __name__)

@app_views.route("/")
def index():
    """
    A simple function to render "Hello World" and status code 200 when the `/`
    endpoint is accessed. Just for testing purposes.
    """
    return "Hello World!"
