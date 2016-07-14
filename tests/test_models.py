"""
Tests for `models.py`.
"""

# pylint: disable=import-error

import unittest

from datetime import datetime

from text_support.app import db
from text_support.models import Texter

class TexterTestCase(unittest.TestCase):
    """
    Tests for the `Texter` model.
    """
    # pylint: disable=missing-super-argument

    def setUp(self):
        """
        Setup to be run before every test.

        We clear the database, and add an entry so one entry already exists.
        """
        Texter.query.delete()

        self._sample_phone_number = "TEST"

        texter = Texter(self._sample_phone_number)
        db.session.add(texter)
        db.session.commit()

    def test_record_new_texter(self):
        """
        Test recording a new texter we have not already seen in the database.
        """
        Texter.record("SOME-NEW-NUMBER")

        texters = Texter.query.all()
        self.assertEqual(len(texters), 2)

    def test_record_update_texter(self):
        """
        Test updating the information for a texter using the record method.
        """
        before_create_time = datetime.utcnow()

        Texter.record(self._sample_phone_number)
        texter = Texter.query.filter_by(phone_number=self._sample_phone_number).first()

        self.assertTrue(texter.text_date > before_create_time)
