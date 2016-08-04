import datetime

class DefaultConfig:
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
	SECRET_KEY = ''
	SESSION_COOKIE_NAME = 'acm-csusb'
	SESSION_KEY_BITS = 256

	JINJA_AUTO_RELOAD = True
	
class DevConfig(DefaultConfig):
	DEBUG = True
	TESTING = True

	SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:dbuser@localhost/db'
	SQLALCHEMY_POOL_SIZE = 1
	