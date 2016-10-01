from .. import db


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
