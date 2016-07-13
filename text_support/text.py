"""
`text.py` is where we contain classes and functions related to texting with the
user.
"""

# pylint: disable=import-error, too-few-public-methods

import os

from twilio.rest import TwilioRestClient

def get_response(message):
    """
    Given what the texter has sent to us, determine our response.

    Args:
        message (str): The message the texter has sent to us.

    Response:
        str: The response we will text back to them.
    """
    # @TODO Fill this function in with code that will have respond.
    return message

def get_text_class():
    """
    Depending on the environment, return a texting instance which we will use to
    send the message.

    Returns:
        Text: The instance to be used by this application.
    """
    env_class_pairs = {
        frozenset({"PRODUCTION"}): TwilioText,
        frozenset({"DEVELOPMENT", "TEST"}): TestText
    }

    env = os.environ["ENVIRONMENT"]

    for env_set, text_class in env_class_pairs.items():
        if env in env_set:
            return text_class

class Text(object):
    """
    The base class for all classes implementing a texting behavior.
    """
    messages_sent = 0

    @classmethod
    def send_message(cls, phone_number, body):
        """
        Send a text message (either through Twilio or through `Test`, which just
        records that a text has been sent).

        Args:
            phone_number (str): The phone_number to which we wish to send the message.
            body (str): The body of the message that we will send.
        """
        # pylint: disable=unused-argument

        cls.messages_sent += 1

class TwilioText(Text):
    """
    A wrapper class for sending text messages with Twilio.
    """
    twilio_client = None

    @classmethod
    def _get_twilio_client(cls):
        """
        A singleton method for getting a twilio rest client.

        Returns:
            TwilioRestClient: The twilio client we'll use for sending text
            messages.
        """
        if not cls.twilio_client:
            account_sid = os.environ["TWILIO_ACCOUNT_SID"]
            auth_token = os.environ["TWILIO_AUTH_TOKEN"]
            cls.twilio_client = TwilioRestClient(account_sid, auth_token)

        return cls.twilio_client

    @classmethod
    def send_message(cls, phone_number, body):
        """
        Send a text message with Twilio.

        Args:
            phone_number(str): The phone number to which we wish to send the message.
            body (str): The body of the message that we will send.
        """
        super(TwilioText, TwilioText).send_message(phone_number, body)

        client = cls._get_twilio_client()
        from_number = os.environ["FROM_NUMBER"]

        client.messages.create(to=phone_number, from_=from_number, body=body)

class TestText(Text):
    """
    A class that we use in testing mode, which doesn't make an actual call to
    twilio, but rather just increases the number of messages sent.
    """
    pass
