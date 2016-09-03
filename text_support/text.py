"""
`text.py` is where we contain classes and functions related to texting with the
user.
"""

# pylint: disable=import-error, too-few-public-methods

import os

from twilio import TwilioRestException
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

def get_follow_up_body():
    """
    Return the follow up text to send to the user reminding them to follow up
    with their friend.

    Returns:
        str: The body of the follow up text to be sent.
    """
    resp = ('Thank you again for texting into Text Support! '
            'If you feel comfortable, consider following up whoever '
            'you were supporting when you texted us.')

    return resp

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

class TextException(Exception):
    """
    An exception caused by attempting to send a text.
    """
    pass

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

        Raises:
            TextException: If fails to successfully send text.
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

        Raises:
            TextException: If failed to send text message.
        """
        super(TwilioText, TwilioText).send_message(phone_number, body)

        client = cls._get_twilio_client()
        from_number = os.environ["FROM_NUMBER"]

        try:
            client.messages.create(to=phone_number, from_=from_number, body=body)
        except TwilioRestException as ex:
            raise TextException(str(ex))

class TestText(Text):
    """
    A class that we use in testing mode, which doesn't make an actual call to
    twilio, but rather just increases the number of messages sent.
    """
    pass
