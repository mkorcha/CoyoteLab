from sqlalchemy.ext.associationproxy import association_proxy
from .. import db


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
	