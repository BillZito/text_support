"""
Tests for `app.py`.
"""

# pylint: disable=import-error

import unittest

from text_support.app import app

class AppTestCase(unittest.TestCase):
    """
    Overarching test cases for the application. Most of the actual testing will
    occur in `test_views.py` or `test_models.py` as we test the handling of web
    requests/working with the database.
    """
    def setUp(self):
        """
        Setup to be run before everytest.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_app_creation(self):
        """
        This test simply checks our blueprints were successfully registered and
        all configuration occured properly.
        """
        self.assertNotEqual(self.app, None)
