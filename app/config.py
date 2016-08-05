import datetime, random, string, redis
from simplekv.memory.redisstore import RedisStore

class DefaultConfig:
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Session configuration
	PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
	SECRET_KEY = ''.join(
			random.SystemRandom().choice(string.printable) for _ in range(32))
	SESSION_COOKIE_NAME = 'acm-csusb'
	SESSION_KEY_BITS = 256
	SESSION_STORE = RedisStore(redis.StrictRedis())

	JINJA_AUTO_RELOAD = True

	# Set higher or lower depending on need
	BCRYPT_WORK_FACTOR = 12
	
	
class DevConfig(DefaultConfig):
	DEBUG = True
	TESTING = True

	# SQL database configuration
	SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:dbuser@localhost/db'
	SQLALCHEMY_POOL_SIZE = 1
	