from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from .enrollment import Enrollment
from .. import db


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
		from ..util.auth import pwhash
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
		return Enrollment.query.filter_by(user=self, course=course, enabled=True).first() is not None
