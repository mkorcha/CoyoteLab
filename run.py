from app import config, get_app


app = get_app(config.DefaultConfig)


if __name__ == '__main__':
	from gevent.pywsgi import WSGIServer
	from geventwebsocket.handler import WebSocketHandler

	server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)

	server.serve_forever()