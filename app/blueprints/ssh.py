from gevent import monkey
monkey.patch_all()

from flask import Blueprint, request, render_template
from werkzeug.exceptions import BadRequest
from wssh import WSSHBridge


blueprint = Blueprint('ssh', __name__, url_prefix='/ssh')


@blueprint.route('/')
def term():
	return render_template('index.html')

@blueprint.route('/socket')
def socket():
	if not request.environ.get('wsgi.websocket'):
		raise BadRequest()

	bridge = WSSHBridge(request.environ['wsgi.websocket'])
	try:
		bridge.open(hostname='10.57.223.64', username='cse', password='cse')
	except:
		request.environ['wsgi.websocket'].close()
		return str()

	bridge.shell()

	request.environ['wsgi.websocket'].close()
	return str()
