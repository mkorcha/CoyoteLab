from flask_wtf import Form 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class UserForm(Form):
	'''
	Form used for adding and updating non-password user information
	'''
	name  = StringField('Name', validators=[DataRequired()])
	email = StringField('Email Address', validators=[DataRequired(), Email()])

	submit = SubmitField('Submit', validators=[DataRequired()])


class UserPasswordForm(Form):
	'''
	Form used for updating a user's password
	'''
	old     = PasswordField('Old Password', validators=[DataRequired()])
	new     = PasswordField('New Password', validators=[DataRequired()])
	confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new', message='Passwords must match'), Length(min=12)])

	submit = SubmitField('Submit', validators=[DataRequired()])
