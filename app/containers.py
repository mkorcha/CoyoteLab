import os
from flask import current_app
from pylxd import Client as LXD

def _get_client():
	'''
	Returns an LXD client object to interact with containers. Returns None if
	a trusted connection cannot be established
	'''
	client = LXD(endpoint=current_app.config['LXD_ADDRESS'], 
		         cert=(os.path.join(os.getcwd(), 'lxd.crt'), os.path.join(os.getcwd(), 'lxd.key')),
		         # we have a self-signed cert, this is fine for development purposes
		         verify=False)
	client.authenticate(current_app.config['LXD_TRUST_PASSWORD'])

	return client if client.trusted else None
