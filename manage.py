"""
`manage.py` contains the files for running migrations of the database.

This allows us to run `python manage.py db init` and `python manage.py db
upgrate` for database tasks.
"""

# pylint: disable=import-error, invalid-name, unused-import

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from text_support.app import app, db
from text_support.config import environment_config
from text_support.models import Texter

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

if __name__ == "__main__":
    manager.run()
