"""
`manage.py` contains the files for running migrations of the database.

This allows us to run `python manage.py db init` and `python manage.py db
upgrate` for database tasks.
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
    Run with `python manage.py create_db`.
    This command will create the applications database.
    """
    db.create_all()

@manager.command
def batch_follow_up_texts():
    """
    Run with `python manage.py batch_follow_up_texts`

    Send all of the necessary follow up texts to `Texters`.
    """
    res = send_follow_up_texts()

    if res.failed > 0:
        err = ('Error: {failure} failues '
               'and {success} successes.').format(failure=res.failed,
                                                  success=res.successful)

        sys.exit(err)

if __name__ == "__main__":
    manager.run()
