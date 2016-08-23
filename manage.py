import datetime
from flask_script import Manager, Shell, prompt_bool
from flask_migrate import MigrateCommand
from app import config, db, get_app, models, auth
from app.models import User, Course
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
	test_user.username = 'mike-i'
	test_user.password = 'password123'
	test_user.email = 'test@weblab1.grad.cse.csusb.edu'
	test_user.name = 'Mike'
	test_user.roles = auth.ROLE_INSTRUCTOR
	db.session.add(test_user)
	db.session.commit()

	test_user2 = User()
	test_user2.username = 'mike-s'
	test_user2.password = 'password123'
	test_user2.email = 'test2@weblab1.grad.cse.csusb.edu'
	test_user2.name = 'Mike'
	test_user2.roles = auth.ROLE_STUDENT
	db.session.add(test_user2)
	db.session.commit()

	test_course = Course()
	test_course.name = 'CSE 201-01'
	test_course.instructor = test_user
	test_course.start_date = datetime.datetime.today()
	test_course.end_date = datetime.datetime.today() + datetime.timedelta(days=5)
	test_course.students.append(test_user2)
	db.session.add(test_course)
	db.session.commit()

	print("Sample data generated")


@manager.command
def test_container():
	from app.containers import _get_client
	print _get_client()

if __name__ == '__main__':
	manager.run()
