"""
Tests for `views.py`.
"""

# pylint: disable=import-error

import unittest

# We register our views as a blueprint with `app` in `app.py`, so it is that app
# we run tests on. See more details
# [here](http://flask.pocoo.org/docs/0.11/blueprints/).
from text_support.app import app
from text_support.models import Texter
from text_support.text import get_text_class

class AppViewsTestCase(unittest.TestCase):
    """
    Test the views within the application.

    All tests of views will inherit from this class.
    """
    def setUp(self):
        """
        Setup to be run before everytest.
        """
        self.app = app.test_client()
        self.app.testing = True

class IndexTestCase(AppViewsTestCase):
    """
    Test accessing the index route ("/").
    """
    def test_index_success(self):
        """
        Test a request to `/` is successful (i.e. returns the status code 200).
        """
        index_url = "/"
        result = self.app.get(index_url)

        self.assertEqual(result.status_code, 200)

class WebhookTestCase(AppViewsTestCase):
    """
    Test post request Twilio will make to `/webhook` when receiving a text
    message.
    """
    # pylint: disable=missing-super-argument

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._webhook_url = "/webhook"

    def setUp(self):
        """
        Clear the database.
        """
        super().setUp()
        Texter.query.delete()

    def test_post_webhook_success(self):
        """
        A successful post to webhook should send a text message, create (or
        update) a `Texter` entry in the database, and return a status code of
        201.

        @TODO These tests could be a lot more thorough, but I will expand them
        once I determine all of the functionality for the `/webhook` route.
        """
        post_body = dict(
            From="+18148264053",
            Body="Test"
        )

        previous_texts_sent = get_text_class().messages_sent
        result = self.app.post(self._webhook_url, data=post_body)

        self.assertEqual(result.status_code, 201)
        self.assertEqual(previous_texts_sent + 1, get_text_class().messages_sent)
        self.assertEqual(len(Texter.query.all()), 1)

