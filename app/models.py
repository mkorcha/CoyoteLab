from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from . import db


class User(db.Model):
	'''
	Model representing a user
	'''
	id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(32),  unique=True, nullable=False)
	password = db.Column(db.String(255), nullable=False)
	email    = db.Column(db.String(255), unique=True, nullable=False)
	name     = db.Column(db.String(255))
	roles    = db.Column(db.Integer, nullable=False, default=0)

	taught   = db.relationship('Course', backref='instructor', lazy='joined')
	enrolled = association_proxy('enrollment_assoc', 'course')

	def has_role(self, role):
		'''
		Checks if the user has a role
		'''
		return bool(self.roles & role)

	def active_in(self, course):
		return Enrollment.query.filter_by(user=self, course=course, enabled=True).first() != None


class Course(db.Model):
	'''
	Model representing a course
	'''
	id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name          = db.Column(db.String(255), nullable=False)
	webpage       = db.Column(db.String(255))
	description   = db.Column(db.Text())
	instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	start_date    = db.Column(db.DateTime(), nullable=False)
	end_date      = db.Column(db.DateTime(), nullable=False)

	students = association_proxy('enrollment_assoc', 'user')
	

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
