from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, URL
from validators import IsAfter


class CourseForm(Form):
	'''
	Form used for adding and updating course information
	'''
	name        = StringField('Name', validators=[DataRequired()])
	webpage     = StringField('Course Webpage')
	description = TextAreaField('Description')
	start_date  = DateField('Start Date', validators=[DataRequired()], description="Format: YYYY-MM-DD")
	end_date    = DateField('End Date', validators=[DataRequired(), IsAfter('start_date')], description="Format: YYYY-MM-DD")

	submit = SubmitField('Submit', validators=[DataRequired()])
