from . import db


class User(db.Model):
	'''
	Model representing a user
	'''
	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32),  unique=True)
	password = db.Column(db.String(255), unique=True)
	email    = db.Column(db.String(255), unique=True)
	name     = db.Column(db.String(255))
	roles    = db.Column(db.Integer)
