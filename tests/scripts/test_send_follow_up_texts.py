"""
Test the script to send the follow up texts.
"""

# pylint: disable=no-member

import unittest

from datetime import datetime, timedelta

from text_support.app import db
from text_support.config import environment_config
from text_support.models import Texter
from text_support.scripts.send_follow_up_texts import main as send_follow_up_texts
from text_support.text import get_text_class

class SendFollowUpTextsTestCase(unittest.TestCase):
    """
    Testing that follow up texts are only sent to the appropriate users.
    """
    def setUp(self):
        """
        Setup to be run before every tests.

        Mostly just cleaning out the database.
        """
        Texter.query.delete()

        cutoff_days = environment_config().CUTOFF_DAYS

        self._in_cutoff = Texter('IN_CUTOFF')
        self._in_cutoff.text_date = datetime.utcnow() - timedelta(days=cutoff_days,
                                                                  hours=3)

        # Our cutoff is one week.
        self._out_cutoff = Texter('OUT_CUTOFF')
        self._out_cutoff.text_date = datetime.utcnow()

        db.session.add_all([self._in_cutoff, self._out_cutoff])
        db.session.commit()

    def test_sends_to_in_range_texters(self):
        """
        We want to send only to texters that have received texts within the last
        week.

        Only one texter was within the range, so only one text should be sent.
        """
        previous_texts = get_text_class().messages_sent
        send_follow_up_texts()

        self.assertEqual(previous_texts + 1, get_text_class().messages_sent)

    def test_deletes_texters_after_send(self):
        """
        After we send a follow up text to the texter, we delete them from the
        database.

        Only one texter was within the range, so only one texter should be
        deleted.
        """
        start_count = len(Texter.query.all())
        send_follow_up_texts()

        self.assertEqual(start_count - 1, len(Texter.query.all()))
