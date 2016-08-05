import datetime, random, string, redis
from simplekv.memory.redisstore import RedisStore

class DefaultConfig:
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
	SECRET_KEY = ''.join(
			random.SystemRandom().choice(string.printable) for _ in range(32))
	SESSION_COOKIE_NAME = 'acm-csusb'
	SESSION_KEY_BITS = 256

	JINJA_AUTO_RELOAD = True

	BCRYPT_WORK_FACTOR = 12

	SESSION_STORE = RedisStore(redis.StrictRedis())
	
	
class DevConfig(DefaultConfig):
	DEBUG = True
	TESTING = True

	SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:dbuser@localhost/db'
	SQLALCHEMY_POOL_SIZE = 1
	