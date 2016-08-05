import bcrypt
from models import User, Role
from flask import current_app, session


def authenticate(username, password):
	'''
	Returns the User if the supplied credentials are correct, None otherwise
	'''
	user = User.query.filter_by(username=id).first()

	if user and bcrypt.checkpw(password, user.password):
		return user

	return None

def login(user):
	'''
	Logs in the user. It's advisable to call authenticate() first, to ensure
	the user being logged in is actually a user and has credentials
	'''
	if user:
		session['user'] = user

def logout():
	'''
	Logs out the currently logged in user
	'''
	session.destroy()

def authenticated():
	'''
	Returns if the user is authenticated 
	'''
	return session.has_key('user') and session['user'] != None

def hash(password):
	'''
	Returns a password hash created with bcrypt that is safe to store
	'''
	password = bytes(password, encoding='utf-8')
	salt = bcrypt.gensalt(rounds=current_app.config['BCRYPT_WORK_FACTOR'])
	return bcrypt.hashpw(password, salt)

def require_login():
	'''
	Decorator that requires a user be logged in to access a given functionality
	'''
	# TODO
	pass

def require_role(rank_id):
	'''
	Decorator that requires a user have a particular role to access a given
	functionality
	'''
	# TODO
	pass
