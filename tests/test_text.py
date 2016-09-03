"""
Tests for `text.py`.
"""

# pylint: disable=import-error

import unittest

from text_support.text import get_response, get_follow_up_body

class GetResponseTestCase(unittest.TestCase):
    """
    Tests for the `views:get_response` method which given the texter's input,
    determines what we will respond.
    """
    def test_sample_test(self):
        """
        This is just a sample test to serve as a template..

        @TODO Delete and replace with other tests.
        """
        message = "test"
        self.assertEqual(message, get_response(message))

    def test_follow_up_body(self):
        """
        Test the follow up we send to the texter if they texted within the last
        week.
        """
        resp = get_follow_up_body()

        self.assertTrue(isinstance(resp, str))
        self.assertTrue(len(resp) > 0)
