"""
`views.py` is where we define the routes of this application.
"""

# pylint: disable=import-error, invalid-name

from flask import Blueprint, render_template, request, Response

from .text import get_response

# We define `static_views` as a Blueprint so that we can import the views in
# `app.py`. This allows all of the `view` logic to be stored in a single file.
# Read more [here](http://flask.pocoo.org/docs/0.11/blueprints/).
static_views = Blueprint("static_views", __name__)

@static_views.route("/")
def index():
    """
    Render `templates/index.html` with a status code of 200.

    Returns:
        object: The rendered template.
    """
    return render_template("index.html")

# We define `webhook_views` as the views handling the webhook which Twilio will
# use to alert us whenever there is a new text to our service.
webhook_views = Blueprint("webhook_views", __name__)

@webhook_views.route("/webhook", methods=["POST"])
def webhook():
    """
    Twilio will make a post request to `/webhook` everytime if receives a new
    text message. This endpoint should both record the texter in the database,
    and use Twilio to send a response. The status code will be 201 if
    successful, and have an appropriate error code if not.

    Returns:
        object: The rendered JSON response.
    """
    # pylint: disable=unused-variable

    if not request.json:
        return Response(status=400)

    # @TODO Finalize these are correct, and also set up the actual webhook on
    # Twilio.
    phone_number = request.json["From"]
    message_body = request.json["Body"]

    # Write phone_number to db in `Texter`.

    response = get_response(message_body)

    # Send the message with text.send(phone_number, response).
    # `text` is an instance of the `Text` class we'll write, which
    # just wraps around Twilio.

    return Response(status=200)
