from . import db


user_roles = db.Table('user_roles',
	db.Column('user', db.Integer, db.ForeignKey('user.id')),
	db.Column('role', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model):
	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32),  unique=True)
	password = db.Column(db.String(255), unique=True)
	email    = db.Column(db.String(255), unique=True)
	name     = db.Column(db.String(255))
	
	roles    = db.relationship('Role', secondary=user_roles, backref='users')

class Role(db.Model):
	id   = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255), unique=True)
