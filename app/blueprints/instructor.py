from flask import Blueprint, session, redirect, render_template, url_for, flash, abort
from ..auth import authenticated, session_user, ROLE_INSTRUCTOR
from ..models import Course, Enrollment
from ..forms.course import CourseForm
from .. import db


blueprint = Blueprint('instructor', __name__, url_prefix='/instructor')


def get_course(course_id):
	'''
	Returns a course from the given course_id if the course is taught by the
	currently authenticated user. Otherwise, the application will display a 404
	error
	'''
	course = Course.query.filter_by(id=course_id, instructor=session_user()).first()

	if course == None:
		abort(404)

	return course


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


@blueprint.route('/course/<course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
	course = get_course(course_id)
	form = CourseForm(obj=course)

	if form.validate_on_submit():
		form.populate_obj(course)

		db.session.commit()

		flash('Course updated')

		return redirect(url_for('instructor.courses'))

	return render_template('courses/edit.jinja', form=form)


@blueprint.route('/course/<course_id>/students')
def students(course_id):
	course = get_course(course_id)
	return render_template('courses/students.jinja', course=course)


@blueprint.route('/course/<course_id>/students/add')
def add_student(course_id):
	pass


@blueprint.route('/course/<course_id>/students/add_many')
def add_many_students(course_id):
	pass	


@blueprint.route('/course/<course_id>/students/activate/<user_id>')
def toggle_enrollment(course_id, user_id):
	enrollment = Enrollment.query.filter_by(course_id=course_id, user_id=user_id).first()

	# make sure the user is part of the course and that the instructor is in 
	# fact the owner of the course
	if enrollment == None or enrollment.course.instructor != session_user():
		abort(404)

	enrollment.enabled = not enrollment.enabled

	db.session.commit()

	flash(enrollment.user.name + ' updated')

	return redirect(url_for('instructor.students', course_id=course_id))
