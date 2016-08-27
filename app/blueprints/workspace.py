from flask import Blueprint


blueprint = Blueprint('workspace', __name__, url_prefix='/workspace')


@blueprint.route('/<course_id>')
def workspace(course_id):
	pass


@blueprint.route('/<course_id>/reset')
def reset(course_id):
	pass


@blueprint.route('/<course_id>/reboot')
def reboot(course_id):
	pass


@blueprint.route('/<course_id>/pulse')
def pulse(course_id):
	pass
	