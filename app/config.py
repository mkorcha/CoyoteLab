import datetime, redis
from simplekv.memory.redisstore import RedisStore
from util import rand_str

class DefaultConfig:
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	PREFERRED_URL_SCHEME = 'https'

	# Session configuration
	PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
	SECRET_KEY = rand_str(32)
	SESSION_COOKIE_NAME = 'coyotelab'
	SESSION_KEY_BITS = 256
	SESSION_STORE = RedisStore(redis.StrictRedis())

	JINJA_AUTO_RELOAD = True

	# Set higher or lower depending on need
	BCRYPT_WORK_FACTOR = 12

	# Mail config
	MAIL_DEFAULT_SENDER = 'mikekorcha@gmail.com'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = ''
	MAIL_PASSWORD = ''

	# LXD config
	LXD_ADDRESS = 'https://localhost:8443'
	LXD_TRUST_PASSWORD = 'lxd_password'
	LXD_LIMIT_MEMORY = '64MB'
	LXD_LIMIT_CPU = '1'

	# The following are templates, with the following parameters:
	# {user_id} - a user's ID
	# {course_id} - a course ID
	USER_COURSE_FILE_DIR = '/var/lib/lxd/containers/user-c{course_id}-u{user_id}/rootfs/home/coyote'
	USER_CONTAINER_NAME = 'user-c{course_id}-u{user_id}'
	

class DevConfig(DefaultConfig):
	DEBUG = True
	TESTING = True

	# SQL database configuration
	SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:dbuser@localhost/db'
	SQLALCHEMY_POOL_SIZE = 1


class DockerConfig(DevConfig):
	# use Redis container
	SESSION_STORE = RedisStore(redis.StrictRedis(host='redis'))

	# use Postgres container
	SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:dbuserpassword@postgres/coyotedb'

	USER_COURSE_FILE_DIR = '../files/user-c{course_id}-u{user_id}/rootfs/home/coyote'
	