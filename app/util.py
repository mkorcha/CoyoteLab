import random, string, os
from functools import wraps
from flask import redirect, url_for, current_app
from pylxd import Client as LXD
from auth import authenticated

def rand_str(length):
	'''
	Returns a random string of given length
	'''
	return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))

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

def lxd_client():
	'''
	Returns an LXD client object to interact with containers. Returns None if
	a trusted connection cannot be established
	'''
	client = LXD(endpoint=current_app.config['LXD_ADDRESS'], 
		         cert=(os.path.join(os.getcwd(), 'cert.crt'), os.path.join(os.getcwd(), 'cert.key')),
		         # we have a self-signed cert, this is fine for development purposes
		         verify=False)
	client.authenticate(current_app.config['LXD_TRUST_PASSWORD'])

	return client if client.trusted else None
