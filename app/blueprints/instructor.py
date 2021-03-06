from flask import Blueprint, session, redirect, render_template, url_for, flash, abort, current_app
from flask_mail import Message as Email

from .. import db, mail
from ..forms.course import CourseForm
from ..forms.students import StudentFileForm
from ..forms.user import UserForm
from ..models import User, Course, Enrollment, Machine
from ..util.auth import authenticated, session_user, ROLE_INSTRUCTOR, ROLE_STUDENT
from ..util.str import rand_str


blueprint = Blueprint('instructor', __name__, url_prefix='/instructor')


def get_course(course_id):
	'''
	Returns a course from the given course_id if the course is taught by the
	currently authenticated user. Otherwise, the application will display a 404
	error
	'''
	course = Course.query.filter_by(id=course_id, instructor=session_user()).first()

	if course is None:
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
	'''
	Handles displaying an instructors courses
	'''
	return render_template('courses/instructor.jinja', courses=session_user().taught)


@blueprint.route('/course/add', methods=['GET', 'POST'])
def add_course():
	'''
	View for an instructor to create a new course
	'''
	form = CourseForm()

	if form.validate_on_submit():
		new_course = Course()
		# autopopulation is an amazing thing
		form.populate_obj(new_course)
		new_course.instructor = session_user()
		# currently only one base machine
		new_course.base_machine_id = 1
		
		db.session.add(new_course)
		db.session.commit()

		flash('Course added')

		return redirect(url_for('instructor.courses'))

	return render_template('courses/edit.jinja', form=form)


@blueprint.route('/course/<course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
	'''
	View for an instructor to edit the given course
	''' 
	course = get_course(course_id)
	form = CourseForm(obj=course)

	if form.validate_on_submit():
		form.populate_obj(course)

		db.session.commit()

		flash('Course updated')

		return redirect(url_for('instructor.courses'))

	return render_template('courses/edit.jinja', form=form, course=course)


@blueprint.route('/course/<course_id>/students')
def students(course_id):
	'''
	View for an instructor to manage the students of a given course
	'''
	course = get_course(course_id)
	return render_template('courses/students/list.jinja', course=course)


@blueprint.route('/course/<course_id>/students/add', methods=['GET', 'POST'])
def add_student(course_id):
	'''
	View for an instructor to add a student to a given course. If the student
	already exists, they will just be added to the course
	'''
	form = UserForm()
	course = get_course(course_id)

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user is None:
			# TODO: this may need to be more generalized, as the next view also
			# uses something similar
			user = User()

			form.populate_obj(user)
			# username generation will be changed at some point
			user.username = form.email.data
			password = rand_str(12)
			user.password = password

			message = Email(subject="[CoyoteLab] New Account", recipients=[user.email], html=render_template('email/new_account.jinja', username=user.username, password=password, url=current_app.config['MAIL_BASE_URL'] + url_for('auth.login')))

			db.session.add(user)

			mail.send(message)

		if not course in user.enrolled:
			user.add_role(ROLE_STUDENT)
			course.students.append(user)

		db.session.commit()

		flash('User added')

		return redirect(url_for('instructor.students', course_id=course_id))

	return render_template('courses/students/add.jinja', course=course, form=form)


@blueprint.route('/course/<course_id>/students/add_many', methods=['GET', 'POST'])
def add_many_students(course_id):
	'''
	View for an instructor to add many users to a given course at once. If any
	student is already a user, they will just be added to the course
	'''
	form = StudentFileForm()
	course = get_course(course_id)

	if form.validate_on_submit():
		file = form.file.data.stream.readlines()

		messages = []

		for entry in file:
			entry = entry.strip().split(',')
			name  = entry[0]
			email = entry[1]

			user = User.query.filter_by(email=email).first()

			if user is None:
				user = User()
				password = rand_str(12)

				user.username = email
				user.email = email
				user.password = password
				user.name = name

				messages.append(Email(subject="[CoyoteLab] New Account", recipients=[user.email], html=render_template('email/new_account.jinja', username=user.username, password=password, url=current_app.config['MAIL_BASE_URL'] + url_for('auth.login'))))

				db.session.add(user)

			if not course in user.enrolled:
				user.add_role(ROLE_STUDENT)
				course.students.append(user)

		db.session.commit()

		with mail.connect() as conn:
			for message in messages:
				conn.send(message)

		flash('Operation completed. ' + str(len(file)) + ' users added')

		return redirect(url_for('instructor.students', course_id=course_id))

	return render_template('courses/students/add_many.jinja', course=course, form=form)


@blueprint.route('/course/<course_id>/students/activate/<user_id>')
def toggle_enrollment(course_id, user_id):
	'''
	Handles adding/dropping a given user from a given course
	'''
	enrollment = Enrollment.query.filter_by(course_id=course_id, user_id=user_id).first()

	# make sure the user is part of the course and that the instructor is in 
	# fact the owner of the course
	if enrollment is None or enrollment.course.instructor != session_user():
		abort(404)

	enrollment.enabled = not enrollment.enabled

	db.session.commit()

	flash(enrollment.user.name + ' updated')

	return redirect(url_for('instructor.students', course_id=course_id))
