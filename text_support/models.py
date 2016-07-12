"""
`models.py` is where we will define all of our database models.

This could theoretically become its own module if there become a lot of models,
but I doubt we will have more than just user (and maybe text).
"""

# pylint: disable=no-member

from datetime import datetime

from .app import db

class Texter(db.Model):
    """
    The model representing someone who has texted into the database. We track
    this so that we can send follow up texts.

    Args:
        phone_number (str): The texters phone number.
        text_date (datetime): The last date at which the texter texted in.
    """
    # pylint: disable=too-few-public-methods, invalid-name, undefined-variable

    __tablename__ = "texters"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String())
    text_date = db.Column(db.DateTime)

    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.text_date = datetime.utcnow()

    def __repr__(self):
        """
        Print the `Texter` model as a string.

        Returns:
            str: A string representation.
        """
        return "<Texter {0}>".format(phone_number)
