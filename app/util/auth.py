from functools import wraps

import bcrypt
from flask import current_app, session, redirect, url_for

from ..models import User

# Roles are a finite set of a few different roles. The easy way to do this is
# to just have a bitwise OR operation to grant multiple roles to a user. For
# example, an admin who was also an instructor could be given the role like
# `ROLE_ADMIN | ROLE_INSTRUCTOR`. To check, you mask the user role with the 
# constant like `user.roles & ROLE_ADMIN`
ROLE_STUDENT    = 0b001
ROLE_INSTRUCTOR = 0b010
ROLE_ADMIN      = 0b100


def authenticate(username, password):
	'''
	Returns the User if the supplied credentials are correct, None otherwise
	'''
	user = User.query.filter_by(username=username).first()

	if user and bcrypt.checkpw(password.encode('utf-8'), 
		                       user.password.encode('utf-8')):
		return user

	return None

def login(user):
	'''
	Logs in the user. It's advisable to call authenticate() first, to ensure
	the user being logged in is actually a user and has credentials
	'''
	if user:
		session['user'] = user.id

def logout():
	'''
	Logs out the currently logged in user
	'''
	session.destroy()

def authenticated():
	'''
	Returns if the user is authenticated 
	'''
	return 'user' in session and session['user'] != None

def pwhash(password):
	'''
	Returns a password hash created with bcrypt that is safe to store
	'''
	salt = bcrypt.gensalt(rounds=current_app.config['BCRYPT_WORK_FACTOR'])
	return bcrypt.hashpw(password.encode('utf-8'), salt)

def session_user():
	'''
	Get the currently logged in user
	'''
	return User.query.get(session['user']) if 'user' in session else None

def require_login(route_func):
	'''
	Decorator that requires that a user is logged in, or they will be redirected
	'''
	@wraps(route_func)
	def wrapper(*args, **kwargs):
		if not authenticated():
			return redirect(url_for('auth.login'))
		return route_func(*args, **kwargs)
	return wrapper
	