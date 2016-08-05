from flask_script import Manager, Shell, prompt_bool
from flask_migrate import MigrateCommand
from app import config, db, get_app, models
from app.models import User
from app.auth import pwhash


app = get_app(config.DevConfig)


manager = Manager(app, with_default_commands=False)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell())


@MigrateCommand.command
def reset():
	'Drops everything from the database and creates a fresh set of tables'
	if prompt_bool('Are you sure you want to reset everything?'):
		db.drop_all()
		db.create_all()
		
		print("Database reset")
	else:
		print("Aborted")


@MigrateCommand.command
def populate():
	'Create sample data for development purposes'
	test_user = User()
	test_user.username = 'mike'
	test_user.password = pwhash('password123')
	test_user.email = 'test@weblab1.grad.cse.csusb.edu'
	test_user.name = 'Mike'
	db.session.add(test_user)
	db.session.commit()

	print("Sample data generated")


if __name__ == '__main__':
	manager.run()
