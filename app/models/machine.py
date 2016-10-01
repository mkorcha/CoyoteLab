from datetime import datetime
from flask import current_app
from pylxd.exceptions import LXDAPIException

from .. import db


class Machine(db.Model):
	'''
	Model representing a users machine
	'''
	id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name            = db.Column(db.String(255), unique=True, nullable=False)
	user_id         = db.Column(db.Integer, db.ForeignKey('user.id'))
	base_machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'))
	last_active     = db.Column(db.DateTime())

	base_machine = db.relationship('Machine', backref='inherited', remote_side='Machine.id', lazy='joined')


	@staticmethod
	def get_or_create(user, course):
		'''
		Creates a new container for the given user/course combination and 
		returns a tuple of the form (lxd_container, model)
		'''
		if not user.active_in(course) and course.instructor != user:
			return None

		from ..util.lxd import lxd_client
		lxd = lxd_client()
		
		pair = Machine.get(user, course)

		if pair != None:
			return pair

		name = current_app.config['USER_CONTAINER_NAME'].format(course_id=course.id, user_id=user.id)

		container = lxd.containers.create({
			'name': name,
			'source': {
				'type': 'copy',
				'source': course.base_machine.name
			},
			'config': {
				'limits.cpu': current_app.config['LXD_LIMIT_CPU'],
				'limits.memory': current_app.config['LXD_LIMIT_MEMORY']
			}}, wait=True)

		machine = Machine()
		machine.name = name
		machine.base_machine = course.base_machine
		machine.owner = user
		machine.last_active = datetime.now()

		db.session.add(machine)
		db.session.commit()

		return (container, machine)


	@staticmethod
	def get(user, course):
		'''
		Gets a container/model pair for the given user/course combination. or
		None if it doesn't exist
		'''
		if not user.active_in(course) and course.instructor != user:
			return None

		from ..util.lxd import lxd_client
		lxd = lxd_client()

		name = current_app.config['USER_CONTAINER_NAME'].format(course_id=course.id, user_id=user.id)

		try:
			container = lxd.containers.get(name)
			return (container, Machine.query.filter_by(name=name).first())
		except LXDAPIException:
			return None
			

	@staticmethod
	def delete(user, course):
		'''
		Deletes a container for the given user/course combination
		'''
		if not user.active_in(course) and course.instructor != user:
			return

		container, model = Machine.get(user, course)

		# remove the container from lxd
		if container:
			try:
				container.stop(wait=True)
			except:
				pass
			finally:
				container.delete(wait=True)

		# remove any record of it from the db
		if model:
			db.session.delete(model)
			db.session.commit()
