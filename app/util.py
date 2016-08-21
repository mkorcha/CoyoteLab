import random, string

def rand_str(length):
	return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length))