from app import config, get_app


app = get_app(config.DevConfig)


if __name__ == '__main__':
	from gevent.pywsgi import WSGIServer
	from geventwebsocket.handler import WebSocketHandler

	server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	