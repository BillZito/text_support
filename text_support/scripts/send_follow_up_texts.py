"""
Sends texts to all Texters who have recently texted in, encouraging them to
follow up with their friennd.
"""

# pylint: disable=import-error, no-member

from collections import namedtuple
from datetime import datetime, timedelta

from sqlalchemy import and_

from ..app import db
from ..config import environment_config
from ..models import Texter
from ..text import get_follow_up_body, get_text_class, TextException

Stats = namedtuple('Stats', ['successful', 'failed'])

def main(cutoff_days=environment_config().CUTOFF_DAYS):
    """
    Send texts to all Texters who texted in a week ago, encouraging them to
    follow up with their friend.

    Delete the texter from the database.

    Args:
        cutoff_days(int): The number of days ago for which we will send a follow
        up text.

    Returns:
        Stats : The Stats pertaining to the success of this script.
    """
    now = datetime.utcnow()

    cutoff_date_start = now - timedelta(days=cutoff_days + 1)
    cutoff_date_end = now - timedelta(days=cutoff_days)

    should_send_message = Texter.query.filter(
        and_(Texter.text_date > cutoff_date_start,
             Texter.text_date < cutoff_date_end)).all()

    successful, failed = 0, 0
    text_cls, follow_up_body = get_text_class(), get_follow_up_body()

    for texter in should_send_message:
        try:
            text_cls.send_message(texter.phone_number, follow_up_body)
        except TextException:
            failed += 1
        else:
            db.session.delete(texter)
            db.session.commit()

            successful += 1

    return Stats(successful=successful, failed=failed)
