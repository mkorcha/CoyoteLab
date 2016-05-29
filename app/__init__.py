import os
from . import blueprints
from flask import Flask


app = Flask(__name__,
	        static_folder='../res',
	        template_folder='../res/html')


for bp in dir(blueprints):
	if not bp.startswith('__'):
		app.register_blueprint(getattr(blueprints, bp).blueprint)
