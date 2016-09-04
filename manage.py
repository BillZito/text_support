"""
`manage.py` contains the files for running scripts/tasks on our application.

This allows us to run `python manage.py db init` and `python manage.py db
upgrate` for database tasks, as well as our custom defined tasks (i.e.
`python manage.py batch_follow_up_texts`).
"""

# pylint: disable=import-error, invalid-name, unused-import

import sys

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from text_support.app import app, db
from text_support.config import environment_config
from text_support.models import Texter
from text_support.scripts.send_follow_up_texts import main as send_follow_up_texts

app.config.from_object(environment_config())
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

@manager.command
def create_db():
    """
    Create the applications database.
    """
    db.create_all()

def _handle_follow_up_response(res):
    """
    A helper function to handle the response of the script which sends our
    follow up texts.

    Args:
        res (send_follow_up_texts.Stats): Named tuple with `successful` and
        `failed` fields.
    """
    if res.failed > 0:
        err = ('Error: {failure} failues '
               'and {success} successes.').format(failure=res.failed,
                                                  success=res.successful)

        sys.exit(err)


@manager.command
def batch_follow_up_texts():
    """
    Send all of the necessary follow up texts to `Texters`.
    """
    res = send_follow_up_texts()

    _handle_follow_up_response(res)

@manager.command
def force_follow_up_texts():
    """
    Send all the follow up texts to `Texters`, but only those who have texted
    within the last day. Intended to be used for testing.
    """
    res = send_follow_up_texts(cutoff_days=0)

    _handle_follow_up_response(res)

if __name__ == "__main__":
    manager.run()
