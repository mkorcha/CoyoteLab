import datetime
import os
import redis

from simplekv.memory.redisstore import RedisStore

from .util.str import rand_str


class Config:
	# Flask config
	# set to false in production
	DEBUG = True
	TESTING = True
	JINJA_AUTO_RELOAD = True
	# always prefer https
	PREFERRED_URL_SCHEME = 'https'

	# Password hashing config
	# set higher or lower depending on need
	BCRYPT_WORK_FACTOR = 12

	# Session configuration
	PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)
	SECRET_KEY = rand_str(32)
	SESSION_COOKIE_NAME = 'coyotelab'
	SESSION_KEY_BITS = 256
	SESSION_STORE = RedisStore(redis.StrictRedis(host='redis'))

	# Database config
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://dbuser:dbuserpassword@postgres/coyotedb'
	SQLALCHEMY_POOL_SIZE = 5

	# Mail config
	MAIL_DEFAULT_SENDER = 'mikekorcha@gmail.com'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = ''
	MAIL_PASSWORD = ''
	# used for generating links in emails
	MAIL_BASE_URL = 'https://localhost'

	# LXD config
	LXD_ADDRESS = 'https://'+ os.environ['HOST_IP'] +':8443'
	LXD_TRUST_PASSWORD = 'lxd_password'
	LXD_LIMIT_MEMORY = '64MB'
	LXD_LIMIT_CPU = '1'

	# The following are templates, with the following parameters:
	# {user_id} - a user's ID
	# {course_id} - a course ID
	USER_COURSE_FILE_DIR = '../files/user-c{course_id}-u{user_id}/rootfs/home/coyote'
	USER_CONTAINER_NAME = 'user-c{course_id}-u{user_id}'
