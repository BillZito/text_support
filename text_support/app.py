"""
`app.py` is where we create our Flask application.
"""

# pylint: disable=import-error, invalid-name

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    """
    A simple function to render "Hello World" and status code 200 when the `/`
    endpoint is accessed. Just for testing purposes.
    """
    return "Hello World!"
