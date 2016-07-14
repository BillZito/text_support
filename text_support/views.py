"""
`views.py` is where we define the routes of this application.
"""

# pylint: disable=import-error, invalid-name

from flask import Blueprint, render_template, request, Response

from .models import Texter
from .text import get_response, get_text_class

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

    if not request.values:
        return Response(status=400)

    phone_number = request.values.get("From")
    message_body = request.values.get("Body")

    if None in {phone_number, message_body}:
        return Response(status=400)

    Texter.record(phone_number)

    response = get_response(message_body)
    get_text_class().send_message(phone_number, response)

    return Response(status=201)
