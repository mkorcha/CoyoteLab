from flask import Blueprint, url_for, redirect, flash, render_template, request, current_app
from ..forms.login import LoginForm
from ..forms.user import UserPasswordForm
from ..util import require_login
from .. import auth, db


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
