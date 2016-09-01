Terminal.prototype.wssh = function(wsendpoint) {
	var client = new WSSHClient(),
	    term = this;

	this.write('Connecting...');

	this.on('key', function(key) {
		client.send(key);
	});

	client.connect(wsendpoint, {
		onError: function(error) {
			term.write('Error: ' + error + '\r\n');
		},
		onConnect: function() {
			// Erase our connecting message
			term.write('\r');
		},
		onClose: function() {
			term.write('Connection Reset By Peer');
		},
		onData: function(data) {
			term.write(data);
		}
	});
}

function workspace_init(element, endpoint) {
	var term = new Terminal({cursorBlink: true});

	term.open(element);
	term.fit()

	term.wssh(endpoint);
}
