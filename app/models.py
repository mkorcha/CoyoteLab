from . import db


user_courses = db.Table('user_courses', 
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
	db.Column('course_id', db.Integer, db.ForeignKey('course.id'), nullable=False)
)


class User(db.Model):
	'''
	Model representing a user
	'''
	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32),  unique=True)
	password = db.Column(db.String(255), unique=True)
	email    = db.Column(db.String(255), unique=True)
	name     = db.Column(db.String(255))
	roles    = db.Column(db.Integer)

class Course(db.Model):
	'''
	Model representing a course
	'''
	id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name          = db.Column(db.String(255))
	webpage       = db.Column(db.String(255))
	description   = db.Column(db.Text())
	instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	start_date    = db.Column(db.DateTime())
	end_date      = db.Column(db.DateTime())

	instructor = db.relationship('Instructor', backref=db.backref('courses'))
	students   = db.relationship('User', secondary=user_courses, backref='courses')