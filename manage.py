import datetime, time, os
from flask_script import Manager, Shell, prompt_bool
from flask_migrate import MigrateCommand
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
from geventwebsocket.handler import WebSocketHandler
from subprocess import Popen
from app import config, db, get_app, models, auth
from app.models import User, Course, Machine
from app.auth import pwhash
from app.util import lxd_client, rand_str


if 'DOCKER' in os.environ:
	# fix the config to use the HOST_IP we get as an environment variable
	# when it starts. this makes the assumption that lxd is running on the
	# host
	# TODO: see if there is potentially another way to do this
	docker_config = config.DockerConfig
	docker_config.LXD_ADDRESS = 'https://'+ os.environ['HOST_IP'] +':8443'

	app = get_app(docker_config)
else:
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
	if not Machine.query.all():
		lxd_init()

	machine = Machine.query.filter_by(name='ubuntu-1604').first()

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
	test_course.base_machine = machine
	db.session.add(test_course)
	db.session.commit()

	print("Sample data generated")


@manager.command
def lxd_init():
	lxd = lxd_client()

	if not Machine.query.all() and not lxd.containers.get('ubuntu-1604'):
		base = lxd.containers.create({
				'name': 'ubuntu-1604',
				'source': {
					'type': 'image',
					'protocol': 'simplestreams',
					'server': 'https://images.linuxcontainers.org',
					'alias': 'ubuntu/xenial/amd64'
				}}, wait=True)
				
		base.start(wait=True)

		# wait for network to come online
		while len(base.state().network['eth0']['addresses']) < 2:
			time.sleep(1)

		commands = [['apt-get', 'install', 'openssh-server', 'sudo', 'man', '-y'],
					['useradd', '-m', '-p', 'cs.ePmqxX543E', '-s', '/bin/bash', '-G', 'sudo', 'coyote'],
					['sed', '-i', '$ a\ALL ALL=(ALL) NOPASSWD: ALL', '/etc/sudoers']]

		for command in commands:
			stdout, stderr = base.execute(command)
			print stdout
			print stderr

		base.stop()

		machine = Machine()
		machine.name = base.name
		machine.base_machine = None
		machine.owner = None

		db.session.add(machine)
		db.session.commit()

		print('Base container {name} created and configured'.format(name=base.name))


@manager.command
def adduser(user_type, email, password=None, name=''):
	'Generate user'
	gen_password = rand_str(8) if password == None else password

	user = User()
	user.username = email
	user.password = gen_password
	user.email = email
	user.name = name

	if user_type == 'instructor':
		user.roles = auth.ROLE_INSTRUCTOR
	elif user_type == 'student':
		user.roles = auth.ROLE_STUDENT
	else:
		print('user_type must be either "instructor" or "student"')
		return

	db.session.add(user)
	db.session.commit()

	print('User {name} successfully created with password "{password}"'.format(name=name if len(name) else email, password=gen_password))


@manager.command
def run():
	'Run built-in development server'
	Popen('gulp', shell=True)

	pool   = Pool(2500)
	server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler, spawn=pool)

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass	


if __name__ == '__main__':
	manager.run()
