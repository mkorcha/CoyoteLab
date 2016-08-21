from flask import Blueprint, redirect, render_template, url_for, flash
from ..auth import authenticated, session_user, ROLE_STUDENT


blueprint = Blueprint('student', __name__, url_prefix='/student')


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
	return render_template('courses/student.jinja', courses=user.enrolled)

