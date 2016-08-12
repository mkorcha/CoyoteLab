from sqlalchemy.ext.hybrid import hybrid_property
from . import db


user_courses = db.Table('user_courses', 
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
	db.Column('course_id', db.Integer, db.ForeignKey('course.id'), nullable=False)
)


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
	enrolled = db.relationship('Course', 
		                        secondary=user_courses,
		                        backref=db.backref('_students'),
		                        lazy='joined')

	def has_role(self, role):
		'''
		Checks if the user has a role
		'''
		return bool(self.roles & role)


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

	
	@hybrid_property
	def students(self):
		'''
		Workaround, adding some nice syntax to get students until I figure out the
		proper way to do it
		'''
		return Course.query.get(self.id)._students
	
