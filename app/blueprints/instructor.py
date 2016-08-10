from flask import Blueprint, session, redirect, render_template, url_for
from ..auth import authenticated, session_user, ROLE_INSTRUCTOR
from ..models import Course


blueprint = Blueprint('instructor', __name__, url_prefix='/instructor')


@blueprint.before_request
def filter():
	'''
	Verify that the user has permission to be here
	'''
	if not authenticated() or not session_user().has_role(ROLE_INSTRUCTOR):
		return redirect(url_for('auth.login'))


@blueprint.route('/')
def courses():
	return render_template('courses.jinja', courses=session_user().taught)
