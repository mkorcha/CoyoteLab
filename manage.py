from flask_script import Manager, Shell
from flask_migrate import MigrateCommand
from app import config, db, get_app, models


app = get_app(config.DefaultConfig)


manager = Manager(app, with_default_commands=False)
manager.add_command('migrate', MigrateCommand)
manager.add_command('shell', Shell())


if __name__ == '__main__':
	manager.run()
