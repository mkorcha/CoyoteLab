from gevent import monkey
monkey.patch_all()

import time, os
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, abort, render_template, current_app, send_file
from werkzeug.exceptions import BadRequest
from wssh import WSSHBridge
from ..util.auth import authenticated, session_user
from ..models import Course, Machine, User
from .. import db


blueprint = Blueprint('workspace', __name__, url_prefix='/workspace')


def get_course(course_id):
	'''
	Returns a course if the user is the instructor or an active student in it.
	Otherwise, returns a 404 error
	'''
	course = Course.query.get(course_id)
	user = session_user()

	if course == None or (course.instructor != user and not user.active_in(course)):
		abort(404)

	return course

def get_student(course, student_id):
	'''
	Returns the student if the instructor can access this student's work
	'''
	student = User.query.get(student_id)

	if student == None or course.instructor != session_user() or not student.active_in(course):
		abort(404)

	return student

@blueprint.before_request
def filter():
	'''
	Verify the user is logged in and belongs here
	'''
	if not authenticated():
		return redirect(url_for('auth.login'))


@blueprint.route('/<course_id>')
@blueprint.route('/<course_id>/<student_id>')
def workspace(course_id, student_id=None):
	'''
	The main workspace view
	'''
	course = get_course(course_id)
	student = get_student(course, student_id) if student_id else None

	return render_template('workspace.jinja', course=course, user=student)


@blueprint.route('/<course_id>/connect')
@blueprint.route('/<course_id>/connect/<student_id>')
def connect(course_id, student_id=None):
	'''
	Websocket endpoint to connect to the machine from the web browser. This
	basically creates it's own bridge between the websocket and sshd running
	on the container

	Note: reloading the page is essentially rebooting the machine
	'''
	course = get_course(course_id)
	student = get_student(course, student_id) if student_id else session_user()
	container, model = Machine.get_or_create(student, course)

	# start the machine if need be and wait for the network to come online, 
	# then get the address to connect to
	try:
		container.start(wait=True)
	except:
		# cause the container is already running
		pass

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
	'''
	Recreates the user's machine
	'''
	course = get_course(course_id)

	# note: only do delete because the next connect will recreate the machine
	Machine.delete(session_user(), course)

	return redirect(url_for('workspace.workspace', course_id=course_id))


@blueprint.route('/<course_id>/download')
@blueprint.route('/<course_id>/download/<student_id>')
def download_files(course_id, student_id=None):
	'''
	Creates a zip file of a user's files for a given course and returns it to
	the browser so it can be downloaded
	'''
	course = get_course(course_id)
	user = get_student(course, student_id) if student_id else session_user()
	
	file = BytesIO()
	zipfile = ZipFile(file, 'w', ZIP_DEFLATED)

	path = current_app.config['USER_COURSE_FILE_DIR'].format(user_id=user.id, course_id=course_id)

	for root, dirs, files in os.walk(path):
		for obj in dirs + files:
			file_path = os.path.join(root, obj)
			zipfile.write(file_path, file_path.replace(path, ''))

	zipfile.close()
	file.seek(0)

	return send_file(file, attachment_filename=(course.name + '-' + user.name).replace(' ', '') + '.zip', as_attachment=True, mimetype='application/x-zip-compressed')
