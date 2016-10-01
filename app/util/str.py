import random
import string


def rand_str(length):
	'''
	Returns a random string of given length
	'''
	return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))
