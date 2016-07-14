"""
`models.py` is where we will define all of our database models.

This could theoretically become its own module if there become a lot of models,
but I doubt we will have more than just user (and maybe text).
"""

# pylint: disable=import-error, no-member

import os

from datetime import datetime

from sqlalchemy.ext.declarative import declared_attr

from .app import db

class Texter(db.Model):
    """
    The model representing someone who has texted into the database. We track
    this so that we can send follow up texts. We record one entry for each new
    person texting in. If they have already texted in before, we udpate their
    `text_date`.

    Args:
        phone_number (str): The texters phone number.
        text_date (datetime): The last date at which the texter texted in.
    """
    # pylint: disable=too-few-public-methods, invalid-name, undefined-variable

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

    @declared_attr
    def __tablename__(cls):
        """
        `__tablename__` is used to determine the name of the database table
        containing our `Texter` objects. We want to have separate tables for our
        different environments, and thus we dynamically calculate the value of
        this attribute based on the environment.

        Returns:
            str: The database table name.
        """
        # pylint: disable=no-self-argument, no-self-use

        base_name = "texters"

        env_extension_hash = {
            "DEVELOPMENT": "dev",
            "TEST": "test",
            "PRODUCTION": "prod"
        }

        extension = env_extension_hash[os.environ["ENVIRONMENT"]]
        return base_name + "_" + extension

    @classmethod
    def record(cls, phone_number):
        """
        Record the `phone_number` in the database. If this is the first time
        we've seen the `phone_number` we create a new `Texter` in the database,
        and if we've seen this number before, then we update the `text_date`
        field.

        Args:
            phone_number (str): The phone number of the texter.
        """
        texter = cls.query.filter_by(phone_number=phone_number).first()

        if texter is None:
            texter = cls(phone_number)
            db.session.add(texter)
        else:
            texter.text_date = datetime.utcnow()

        db.session.commit()
