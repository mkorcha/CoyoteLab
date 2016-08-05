import bcrypt
from models import User, Role
from flask import current_app, session


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
	return 'user' in session and session['user'] != None

def pwhash(password):
	'''
	Returns a password hash created with bcrypt that is safe to store
	'''
	salt = bcrypt.gensalt(rounds=current_app.config['BCRYPT_WORK_FACTOR'])
	return bcrypt.hashpw(password.encode('utf-8'), salt)
