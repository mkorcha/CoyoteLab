from flask import Blueprint, render_template


blueprint = Blueprint('main', __name__, url_prefix='/')


@blueprint.route('/')
def hello():
	return render_template('base.jinja')
