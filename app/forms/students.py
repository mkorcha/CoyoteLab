from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from wtforms.validators import DataRequired


class StudentFileForm(Form):
	'''
	Form used to create many students from a CSV file
	'''
	file = FileField('File', validators=[FileRequired(), FileAllowed(['csv'], 'Only CSV files are permitted')])

	submit = SubmitField('Submit', validators=[DataRequired()])
