"""
Tests for `text.py`.
"""

# pylint: disable=import-error, missing-docstring

import unittest

from text_support.text import get_response, get_follow_up_body, CATEGORY_RESPONSES

class GetResponseTestCase(unittest.TestCase):
    """
    Tests for the `views:get_response` method which given the texter's input,
    determines what we will respond.
    """
    def test_follow_up_body(self):
        """
        Test the follow up we send to the texter if they texted within the last
        week.
        """
        resp = get_follow_up_body()

        self.assertTrue(isinstance(resp, str))
        self.assertTrue(len(resp) > 0)

    def test_depression(self):
        message = "depression"
        message_two = "tired"
        answer = CATEGORY_RESPONSES["depression"]
        self.assertEqual(answer, get_response(message))
        self.assertEqual(answer, get_response(message_two))

    def test_recognize_capitals(self):
        """
        We want to match no matter the capitalization that they use.
        """
        message = "Depression"
        answer = CATEGORY_RESPONSES["depression"]

        self.assertEqual(answer, get_response(message))

    def test_sexual_assault(self):
        message = "sex"
        message_two = "survivor"
        answer = CATEGORY_RESPONSES["sexual_assault"]
        self.assertEqual(answer, get_response(message))
        self.assertEqual(answer, get_response(message_two))

    def test_anxiety(self):
        message = "breath"
        answer = CATEGORY_RESPONSES["anxiety"]
        self.assertEqual(answer, get_response(message))

    def test_eating(self):
        message = "exercise"
        answer = CATEGORY_RESPONSES["eating_disorder"]
        self.assertEqual(answer, get_response(message))


    def test_mixed(self):
        """
        If there is a message with multiple keywords, the response
        should be for the category with the most keywords.
        """
        most_depressed = "went to park, depressed, tired, sex, eat"
        answer_depress = CATEGORY_RESPONSES["depression"]

        #if equal, should be the first category listed in our category_resp.
        most_sex = "sex, assault, panic, nervous, hookup"
        answer_sex = CATEGORY_RESPONSES["sexual_assault"]

        self.assertEqual(answer_depress, get_response(most_depressed))
        self.assertEqual(answer_sex, get_response(most_sex))

    def test_edge(self):
        """
        If there is an empty message sent (or one with no keywords), it should
        return the unknown response, which asks what the issue is the user is
        helping their friend with
        """
        message = ""
        answer = CATEGORY_RESPONSES["unknown"]
        self.assertEqual(answer, get_response(message))

