from flask import Blueprint, url_for, redirect, flash, render_template, request, current_app
from flask_mail import Message as Email
from ..forms.login import LoginForm
from ..forms.user import UserPasswordForm, PasswordResetForm
from ..models import User
from ..util import require_login, rand_str
from .. import auth, db, mail


blueprint = Blueprint('auth', __name__)


@blueprint.before_app_request
def filter():
	'''
	Verifies that the user is authenticated and does not need to change a
	temporary password. This is an application-wide filter
	'''
	# add a couple of helpers for the base template so that I don't have to pass
	# in a bunch of stuff each time
	# TODO: I feel like there is a better way to do this
	current_app.jinja_env.globals['authenticated'] = auth.authenticated
	current_app.jinja_env.globals['current_user']  = lambda: auth.session_user()
	current_app.jinja_env.globals['is_instructor'] = lambda: auth.session_user().has_role(auth.ROLE_INSTRUCTOR)
	current_app.jinja_env.globals['is_student']    = lambda: auth.session_user().has_role(auth.ROLE_STUDENT)

	if auth.authenticated() and auth.session_user().temporary_pw and not request.path in ['/logout', '/change_pw']:
		return redirect(url_for('auth.change_password'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
	'''
	Handles logging the user in
	'''
	if auth.authenticated():
		return redirect(url_for('instructor.courses'))

	form = LoginForm()

	if form.validate_on_submit():
		user = auth.authenticate(form.username.data, form.password.data)

		if user:
			auth.login(user)

			if user.has_role(auth.ROLE_STUDENT):
				return redirect(url_for('student.courses'))

			if user.has_role(auth.ROLE_INSTRUCTOR):
				return redirect(url_for('instructor.courses'))

			return redirect(url_for('main.hello'))
		else:
			flash('Invalid credentials.')

	return render_template('login.jinja', form=form)


@blueprint.route('/logout')
def logout():
	'''
	Handles logging the user out
	'''
	if auth.authenticated():
		auth.logout()
		flash('You have been logged out.')

	return redirect(url_for('auth.login'))


@blueprint.route('/change_pw', methods=['GET', 'POST'])
@require_login
def change_password():
	'''
	Handles a user's password change
	'''
	form = UserPasswordForm()

	if form.validate_on_submit():
		user = auth.session_user()
		user.password = form.new.data
		user.temporary_pw = False

		db.session.commit()

		auth.logout()

		flash('Password successfully changed. Please relogin.')

		return redirect(url_for('auth.login'))

	return render_template('user/change_pw.jinja', form=form)


@blueprint.route('/forgot_pw', methods=['GET', 'POST'])
def forgot_password():
	'''
	Handles a user who forgot their password
	'''
	form = PasswordResetForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user:
			password = rand_str(12)

			user.password = password
			user.temporary_pw = True

			message = Email(subject='[CoyoteLab] Password Reset', recipients=[user.email], html=render_template('email/reset_pw.jinja', password=password, url=current_app.config['MAIL_BASE_URL'] + url_for('auth.login')))

			db.session.commit()

			mail.send(message)

		flash('Instructions to reset your password have been sent to the email provided.')

		return redirect(url_for('auth.login'))

	return render_template('user/reset_pw.jinja', form=form)
