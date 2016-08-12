from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, URL


class CourseForm(Form):
	'''
	Form used for adding and updating course information
	'''
	name        = StringField('Name', validators=[DataRequired()])
	webpage     = StringField('Course Webpage', validators=[URL()])
	description = TextAreaField('Description')
	start_date  = DateField('Start Date', validators=[DataRequired()])
	end_date    = DateField('End Date', validators=[DataRequired()])

	submit = SubmitField('Log In', validators=[DataRequired()])
