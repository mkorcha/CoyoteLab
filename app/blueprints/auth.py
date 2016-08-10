from flask import Blueprint, url_for, redirect, flash, render_template
from .. import auth
from ..forms.login import LoginForm


blueprint = Blueprint('auth', __name__)


@blueprint.route('/courses')
def courses():
	'''
	Placeholder for courses view
	'''
	if auth.authenticated():
		return "logged in!"
	else:
		return "logged out!"


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

			return redirect(url_for('instructor.courses'))
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
