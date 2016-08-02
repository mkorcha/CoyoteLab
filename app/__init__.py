import os
from . import blueprints
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


db = SQLAlchemy()
migrate = Migrate()


def get_app(config):
	app = Flask(__name__,
		        static_folder='../res',
		        template_folder='../res/html')
	app.config.from_object(config)

	for bp in dir(blueprints):
		if not bp.startswith('__'):
			app.register_blueprint(getattr(blueprints, bp).blueprint)


	db.init_app(app)
	migrate.init_app(app)
