from gevent import monkey
monkey.patch_all()

import time
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, abort, render_template
from werkzeug.exceptions import BadRequest
from wssh import WSSHBridge
from ..auth import authenticated, session_user
from ..models import Course, Machine
from .. import db

blueprint = Blueprint('workspace', __name__, url_prefix='/workspace')


def get_course(course_id):
	'''
	Returns a course if the user is the instructor or an active student in it.
	Otherwise, returns a 404 error
	'''
	course = Course.query.get(course_id)
	user = session_user()

	if course.instructor != user and not user.active_in(course):
		abort(404)

	return course


@blueprint.before_request
def filter():
	'''
	Verify the user is logged in and belongs here
	'''
	if not authenticated():
		return redirect(url_for('auth.login'))


@blueprint.route('/<course_id>')
def workspace(course_id):
	course = get_course(course_id)
	return render_template('workspace.jinja', course=course)


@blueprint.route('/<course_id>/connect')
def connect(course_id):
	'''
	Websocket endpoint to connect to the machine from the web browser. This
	basically creates it's own bridge between the websocket and sshd running
	on the container
	'''
	course = get_course(course_id)
	container, model = Machine.get_or_create(session_user(), course)

	# start the machine if need be and wait for the network to come online, 
	# then get the address to connect to
	container.start(wait=True)

	while len(container.state().network['eth0']['addresses']) < 2:
		time.sleep(1)

	for addr in container.state().network['eth0']['addresses']:
		if addr['family'] == 'inet':
			address = addr['address']

	model.last_active = datetime.now()
	db.session.commit()

	# if we can't use websockets, there is a serious issue...
	if not request.environ.get('wsgi.websocket'):
		raise BadRequest()

	bridge = WSSHBridge(request.environ['wsgi.websocket'])

	try:
		bridge.open(hostname=address, username='coyote', password='coyote')
	except:
		request.environ['wsgi.websocket'].close()

		container.stop()

		model.last_active = datetime.now()
		db.session.commit()

		return str()

	bridge.shell()

	request.environ['wsgi.websocket'].close()

	# once it's closed, we want to stop the machine to get back the resources
	container.stop()

	model.last_active = datetime.now()
	db.session.commit()

	return str()


@blueprint.route('/<course_id>/reset')
def reset(course_id):
	pass


@blueprint.route('/<course_id>/reboot')
def reboot(course_id):
	pass


@blueprint.route('/<course_id>/pulse')
def pulse(course_id):
	pass
	