from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
	'''
	Form used to perform a user login
	'''
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])

	submit = SubmitField('Log In', validators=[DataRequired()])
	