from datetime import datetime
from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from pylxd.exceptions import LXDAPIException
from . import db


class User(db.Model):
	'''
	Model representing a user
	'''
	id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username     = db.Column(db.String(32),  unique=True, nullable=False)
	# flags if the password is temporary and needs to be changed
	temporary_pw = db.Column(db.Boolean, default=True)
	email        = db.Column(db.String(255), unique=True, nullable=False)
	name         = db.Column(db.String(255))
	roles        = db.Column(db.Integer, nullable=False, default=0)

	# accessed and set via a hybrid property 'password'
	_password = db.Column('password', db.String(255), nullable=False)

	taught   = db.relationship('Course', backref='instructor', lazy='joined')
	enrolled = association_proxy('enrollment_assoc', 'course')
	machines = db.relationship('Machine', backref='owner', lazy='dynamic')


	@hybrid_property
	def password(self):
		'''
		Returns the password hash field
		'''
		return self._password


	@password.setter
	def password(self, value):
		'''
		Sets the password to the hash of the provided value
		'''
		from .auth import pwhash
		self._password = pwhash(value)


	@password.deleter
	def password(self):
		'''
		Removes the password key from the model
		'''
		del self._password

	def has_role(self, role):
		'''
		Checks if the user has a role
		'''
		return bool(self.roles & role)

	def add_role(self, role):
		'''
		Adds a role to a user
		'''
		if self.roles:
			self.roles |= role
		else:
			self.roles = role

	def active_in(self, course):
		'''
		Returns whether a user is active in a course or not via the association
		table
		'''
		return Enrollment.query.filter_by(user=self, course=course, enabled=True).first() != None


class Course(db.Model):
	'''
	Model representing a course
	'''
	id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name            = db.Column(db.String(255), nullable=False)
	webpage         = db.Column(db.String(255))
	description     = db.Column(db.Text())
	instructor_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	start_date      = db.Column(db.DateTime(), nullable=False)
	end_date        = db.Column(db.DateTime(), nullable=False)
	base_machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)

	students     = association_proxy('enrollment_assoc', 'user')
	base_machine = db.relationship('Machine', backref=db.backref('course', uselist=False))
	

class Enrollment(db.Model):
	'''
	Model handling the association between a user and the courses they are 
	enrolled in in a many-to-many relationship, with some added data
	'''
	__tablename__ = 'user_courses'

	user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
	enabled   = db.Column(db.Boolean, default=True)

	user   = db.relationship('User', backref='enrollment_assoc')
	course = db.relationship('Course', backref='enrollment_assoc')

	def __init__(self, user=None, course=None, enabled=True):
		self.user    = user
		self.course  = course
		self.enabled = enabled


class Machine(db.Model):
	'''
	Model representing a users machine
	'''
	id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name            = db.Column(db.String(255), unique=True, nullable=False)
	user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
	base_machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
	last_active     = db.Column(db.DateTime())

	base_machine = db.relationship('Machine', backref='inherited', remote_side='Machine.id', lazy='joined')


	@staticmethod
	def get_or_create(user, course):
		'''
		Creates a new container for the given user/course combination and 
		returns a tuple of the form (lxd_container, model)
		'''
		if not user.active_in(course) and course.instructor != user:
			# TODO: raise an exception
			return None

		from util import lxd_client
		lxd = lxd_client()
		
		name = current_app.config['USER_CONTAINER_NAME'].format(course_id=course.id, user_id=user.id)

		try:
			container = lxd.containers.get(name)
			return (container, Machine.query.filter_by(name=name).first())
		except LXDAPIException:
			pass

		container = lxd.containers.create({
			'name': name,
			'source': {
				'type': 'copy',
				'source': course.base_machine.name
			},
			'config': {
				'limits.cpu': current_app.config['LXD_LIMIT_CPU'],
				'limits.memory': current_app.config['LXD_LIMIT_MEMORY']
			}}, wait=True)

		container.snapshots.create('original')

		machine = Machine()
		machine.name = name
		machine.base_machine = course.base_machine
		machine.owner = user
		machine.last_active = datetime.now()

		db.session.add(machine)
		db.session.commit()

		return (container, machine)
