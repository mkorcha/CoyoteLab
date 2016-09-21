from wtforms.validators import ValidationError


class IsAfter():
	'''
	Validator that verifies the DateField being validated is after the given
	field
	'''
	def __init__(self, rhs, message=None):
		self.rhs = rhs
		if not message:
			message = 'Must be later than {field}'
		self.message = message

	def __call__(self, form, field):
		if field.data < form[self.rhs].data:
			raise ValidationError(self.message.format(field=form[self.rhs].label.text))

