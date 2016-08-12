from flask import Blueprint, session, redirect, render_template, url_for, flash
from ..auth import authenticated, session_user, ROLE_INSTRUCTOR
from ..models import Course
from ..forms.course import CourseForm
from .. import db


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
	return render_template('courses/main.jinja', courses=session_user().taught)


@blueprint.route('/course/add', methods=['GET', 'POST'])
def add_course():
	form = CourseForm()

	if form.validate_on_submit():
		new_course = Course()
		form.populate_obj(new_course)
		new_course.instructor = session_user()
		
		db.session.add(new_course)
		db.session.commit()

		flash('Course added')

		return redirect(url_for('instructor.courses'))

	return render_template('courses/edit.jinja', form=form)
