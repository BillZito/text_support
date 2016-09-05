"""
`text.py` is where we contain classes and functions related to texting with the
user.
"""

# pylint: disable=import-error, too-few-public-methods

import os

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

CATEGORY_RESPONSES = {
    "depression":
    """Remember 1) depression is a
    serious, and often long-term condition, 2) it's never their fault
    for being depressed. Try saying\"you are important to me. Your
    life is important to me.\"""",
    "sexual_assault":
    """Remember 1) it is never the survivor's fault
    , 2) use the words that the survivor uses and let them guide you.
    Try saying \"It's really hard to share something like this.
    Thank you for sharing with me.\"""",
    "anxiety":
    """Remember 1) it's never their fault for feeling nervous,
    2) talk in a calm and reassuring voice.
    Try saying\"let's take two deep breaths together.\"""",
    "eating_disorder":
    """Remember 1) it is never their fault for feeling
    bad, 2) it is your job to help, not to make them realize a
    problem you think they have. Try saying\"How are you feeling?\""""
}

CATEGORY_RESPONSES["unknown"] = ("Are you helping your friend with"
                                 + ", ".join(CATEGORY_RESPONSES.keys())
                                 + ", or something else?")

def get_response(message):
    """
    Given what the texter has sent to us, determine our response.
    Args:
        message (str): The message the texter has sent to us.

    Use one dictionary to hold counts for each category of keywords,
    and one to hold list of all keywords for that category.
    Given a message, find the most common category and respond given
    a third dict. of responses. If all counts 0, respond asking for
    category.

    Response:
        str: The response we will text back to them.

    """
    category_counts = {"depression":0, "sexual_assault": 0, "anxiety":0,
                       "eating_disorder":0}

    keywords = {"depression": ['depress', 'sad', 'lonely', 'upset', 'tired'],
                "sexual_assault": ['sex', 'assault', 'rape', 'hookup',
                                   'survivor'],
                "anxiety": ['panic', 'anxi', 'nervous', 'afraid', 'breath'],
                "eating_disorder": ['bulimi', 'anorex', 'body', 'eating',
                                    'exercis']
               }

    #for each key/val in keyword, add one to category's count if in message
    for category, keyword_list in keywords.items():
        for keyword in keyword_list:
            if keyword in message.lower():
                category_counts[category] += 1

    #for each category in counts, if larger value, set to new max val/response
    curr_max = 0
    response = CATEGORY_RESPONSES["unknown"]
    for category, count in category_counts.items():
        if count > curr_max:
            curr_max = count
            response = CATEGORY_RESPONSES[category]

    return response

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
