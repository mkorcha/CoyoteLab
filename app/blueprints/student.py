import os
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from flask import Blueprint, redirect, render_template, url_for, flash, abort, current_app, send_file
from ..auth import authenticated, session_user, ROLE_STUDENT
from ..models import Course, Enrollment
from .. import db


blueprint = Blueprint('student', __name__, url_prefix='/student')


def get_course(course_id):
	'''
	Returns a course from the given course ID if the student is enrolled in it,
	otherwise will abort
	'''
	course = Course.query.get(course_id)
	user = session_user()

	if course == None or not course in user.enrolled or not user.active_in(course):
		abort(404)

	return course


@blueprint.before_request
def filter():
	'''
	Verify that the user is logged in and a student, otherwise they shouldn't
	be here

	'''
	if not authenticated() or not session_user().has_role(ROLE_STUDENT):
		return redirect(url_for('auth.login'))


@blueprint.route('/')
def courses():
	# a reference to the user needs to be kept around, otherwise the 
	# association proxy for the enrollment table goes stale
	user = session_user()
	return render_template('courses/student.jinja', courses=[x for x in user.enrolled if user.active_in(x)])


@blueprint.route('/course/<course_id>')
def course_info(course_id):
	course = get_course(course_id)
	return render_template('courses/info.jinja', course=course)


@blueprint.route('/course/<course_id>/drop')
def drop_course(course_id):
	course = get_course(course_id)

	enrollment = Enrollment.query.filter_by(course=course, user=session_user()).first()

	if enrollment == None:
		abort(404)

	enrollment.enabled = False

	db.session.commit()

	flash('Course dropped')

	return redirect(url_for('student.courses'))


@blueprint.route('/course/<course_id>/download')
def download_files(course_id):
	course = get_course(course_id)
	user = session_user()
	
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
