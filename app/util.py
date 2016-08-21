import random, string
from functools import wraps
from flask import redirect, url_for
from auth import authenticated

def rand_str(length):
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
