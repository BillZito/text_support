"""
Tests for `views.py`.
"""

# pylint: disable=import-error

import unittest

# We register our views as a blueprint with `app` in `app.py`, so it is that app
# we run tests on. See more details
# [here](http://flask.pocoo.org/docs/0.11/blueprints/).
from text_support.app import app

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
