import os
from flask import Flask
from flask_kvsession import KVSessionExtension
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect


db = SQLAlchemy()
migrate = Migrate()
csrf = CsrfProtect()
session = KVSessionExtension()


def get_app(config):
	app = Flask(__name__,
		        static_folder='../res',
		        template_folder='../res/templates')
	app.config.from_object(config)

	from . import blueprints

	for bp in dir(blueprints):
		if not bp.startswith('__'):
			app.register_blueprint(getattr(blueprints, bp).blueprint)

	db.init_app(app)
	migrate.init_app(app, db)
	csrf.init_app(app)
	session.init_app(app, app.config['SESSION_STORE'])

	return app
